"""Unit tests for elo.py — runnable with plain `python test_elo.py` (no pytest needed)."""
from __future__ import annotations

import elo


def approx(x: float, y: float, tol: float = 1e-6) -> bool:
    return abs(x - y) <= tol


def test_expected_score_equal_ratings():
    assert approx(elo.expected_score(1200, 1200), 0.5)


def test_expected_score_monotonic():
    # higher-rated player has >0.5 expected score
    assert elo.expected_score(1400, 1200) > 0.5
    assert elo.expected_score(1200, 1400) < 0.5
    # expectations of a pair sum to 1
    assert approx(
        elo.expected_score(1400, 1200) + elo.expected_score(1200, 1400), 1.0
    )


def test_draw_between_equals_no_change():
    a, b = elo.update_pair(1200, 1200, 0.5)
    assert approx(a, 1200) and approx(b, 1200)


def test_win_increases_winner_decreases_loser():
    a, b = elo.update_pair(1200, 1200, 1.0)  # A wins
    assert a > 1200 and b < 1200
    # equal starting ratings + K=32 → ±16
    assert approx(a, 1216) and approx(b, 1184)


def test_zero_sum_points():
    ra, rb = 1300, 1100
    na, nb = elo.update_pair(ra, rb, 1.0)
    assert approx((na - ra) + (nb - rb), 0.0)


def test_upset_moves_more_than_expected_win():
    # underdog (1100) beating favourite (1300) gains more than favourite beating underdog
    _, underdog_after_win = elo.update_pair(1300, 1100, 0.0)  # B (underdog) wins
    fav_after_win, _ = elo.update_pair(1300, 1100, 1.0)  # A (favourite) wins
    underdog_gain = underdog_after_win - 1100
    favourite_gain = fav_after_win - 1300
    assert underdog_gain > favourite_gain


def test_apply_matches_deterministic_and_unknown_ids():
    matches = [
        {"a": "h1", "b": "h2", "winner": "h1"},
        {"a": "h2", "b": "h3", "winner": "draw"},
    ]
    out1 = elo.apply_matches({}, matches)
    out2 = elo.apply_matches({}, matches)
    assert out1 == out2  # deterministic
    assert out1["h1"] > 1200  # won its match
    assert out1["h2"] < 1200  # lost to h1 (small later draw doesn't recover it)
    # h3 drew against a now-lower-rated h2, so it loses a little from base
    assert out1["h3"] < 1200


def test_draw_between_fresh_equals_no_change():
    out = elo.apply_matches({}, [{"a": "x", "b": "y", "winner": "draw"}])
    assert approx(out["x"], 1200) and approx(out["y"], 1200)


def test_standings_sorted_desc():
    s = elo.standings({"a": 1190, "b": 1300, "c": 1205})
    assert [hid for hid, _ in s] == ["b", "c", "a"]


def test_invalid_winner_raises():
    try:
        elo.apply_matches({}, [{"a": "h1", "b": "h2", "winner": "nope"}])
    except ValueError:
        return
    raise AssertionError("expected ValueError for invalid winner")


def main() -> None:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} passed")


if __name__ == "__main__":
    main()
