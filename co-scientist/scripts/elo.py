"""Elo tournament bookkeeping for the Claude Code co-scientist.

Pure standard library — no third-party deps. The deterministic rating math is kept
OUT of the LLM on purpose: the Ranking subagent only decides who wins a pairwise
debate; this module turns those win/loss/draw outcomes into Elo ratings.

Used by the orchestrator skill after each tournament bracket (Phase 2+).

CLI:
    python elo.py --session ../data/<session_id>
        reads  <session>/hypotheses.json  (list of {"id", ...})
               <session>/matches.json      (append-only FULL match history)
        recomputes every hypothesis's Elo from BASE_RATING over the full history,
        writes the result back into hypotheses.json, prints the standings.

The CLI is **idempotent**: it always recomputes from BASE over all matches, so it can be
re-run every round as matches.json grows without double-counting. (Recompute-from-history in
chronological order is equivalent to updating incrementally each round — see test_elo.py.)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BASE_RATING = 1200.0
K_FACTOR = 32.0


def expected_score(rating_a: float, rating_b: float) -> float:
    """Probability that A beats B under the Elo model."""
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))


def update_pair(
    rating_a: float, rating_b: float, score_a: float, k: float = K_FACTOR
) -> tuple[float, float]:
    """Return updated (rating_a, rating_b) after one match.

    score_a is 1.0 (A won), 0.0 (B won) or 0.5 (draw).
    """
    ea = expected_score(rating_a, rating_b)
    eb = expected_score(rating_b, rating_a)
    new_a = rating_a + k * (score_a - ea)
    new_b = rating_b + k * ((1.0 - score_a) - eb)
    return new_a, new_b


def _score_for_a(match: dict) -> float:
    a, b, winner = match["a"], match["b"], match.get("winner")
    if winner == a:
        return 1.0
    if winner == b:
        return 0.0
    if winner in ("draw", "tie", None):
        return 0.5
    raise ValueError(f"match winner {winner!r} is neither {a!r}, {b!r}, nor a draw")


def apply_matches(
    ratings: dict[str, float], matches: list[dict], k: float = K_FACTOR
) -> dict[str, float]:
    """Apply a sequence of matches to a copy of `ratings` and return the result.

    Unknown hypothesis ids start at BASE_RATING. Matches are applied in order.
    """
    out = dict(ratings)
    for m in matches:
        a, b = m["a"], m["b"]
        ra = out.get(a, BASE_RATING)
        rb = out.get(b, BASE_RATING)
        na, nb = update_pair(ra, rb, _score_for_a(m), k)
        out[a], out[b] = na, nb
    return out


def standings(ratings: dict[str, float]) -> list[tuple[str, float]]:
    """Hypothesis ids sorted by Elo, highest first."""
    return sorted(ratings.items(), key=lambda kv: kv[1], reverse=True)


def _run_cli(session: Path) -> None:
    hyps_path = session / "hypotheses.json"
    matches_path = session / "matches.json"
    hyps = json.loads(hyps_path.read_text())
    matches = json.loads(matches_path.read_text())

    # Recompute from BASE over the full history -> idempotent (no double-counting on re-run).
    ratings = {h["id"]: BASE_RATING for h in hyps}
    ratings = apply_matches(ratings, matches)

    for h in hyps:
        h["elo"] = round(ratings[h["id"]], 2)
    hyps_path.write_text(json.dumps(hyps, indent=2) + "\n")

    print(f"Updated {len(hyps)} hypotheses from {len(matches)} matches:\n")
    for rank, (hid, elo) in enumerate(standings(ratings), 1):
        print(f"  {rank:>2}. {hid:<16} {elo:7.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Elo bookkeeping for the co-scientist.")
    parser.add_argument("--session", required=True, type=Path, help="session data dir")
    args = parser.parse_args()
    _run_cli(args.session)


if __name__ == "__main__":
    main()
