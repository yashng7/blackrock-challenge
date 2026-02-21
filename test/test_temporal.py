import pytest
import pandas as pd
from app.engines.temporal import apply_temporal_rules


def make_df(rows):
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


def test_no_periods():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    result = apply_temporal_rules(df, [], [])
    assert result.iloc[0]["remanent"] == 50.0


def test_q_override():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    result = apply_temporal_rules(df, [{"fixed": 90, "start": "2024-01-10 00:00:00", "end": "2024-01-20 00:00:00"}], [])
    assert result.iloc[0]["remanent"] == 90.0


def test_q_override_to_zero():
    df = make_df([{"date": "2023-07-01 12:00:00", "amount": 620.0, "ceiling": 700.0, "remanent": 80.0}])
    result = apply_temporal_rules(df, [{"fixed": 0, "start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59"}], [])
    assert result.iloc[0]["remanent"] == 0.0


def test_q_latest_start_wins():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    q = [
        {"fixed": 75, "start": "2024-01-10 00:00:00", "end": "2024-01-25 00:00:00"},
        {"fixed": 90, "start": "2024-01-14 00:00:00", "end": "2024-01-22 00:00:00"},
    ]
    result = apply_temporal_rules(df, q, [])
    assert result.iloc[0]["remanent"] == 90.0


def test_q_tie_first_listed():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    q = [
        {"fixed": 75, "start": "2024-01-14 00:00:00", "end": "2024-01-25 00:00:00"},
        {"fixed": 90, "start": "2024-01-14 00:00:00", "end": "2024-01-22 00:00:00"},
    ]
    result = apply_temporal_rules(df, q, [])
    assert result.iloc[0]["remanent"] == 75.0


def test_p_addition():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    result = apply_temporal_rules(df, [], [{"extra": 10, "start": "2024-01-01 00:00:00", "end": "2024-01-31 00:00:00"}])
    assert result.iloc[0]["remanent"] == 60.0


def test_p_multiple_sum():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    p = [
        {"extra": 10, "start": "2024-01-01 00:00:00", "end": "2024-01-31 00:00:00"},
        {"extra": 25, "start": "2024-01-10 00:00:00", "end": "2024-01-20 00:00:00"},
    ]
    result = apply_temporal_rules(df, [], p)
    assert result.iloc[0]["remanent"] == 85.0


def test_q_then_p():
    df = make_df([{"date": "2024-01-15 10:30:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0}])
    result = apply_temporal_rules(
        df,
        [{"fixed": 90, "start": "2024-01-10 00:00:00", "end": "2024-01-20 00:00:00"}],
        [{"extra": 10, "start": "2024-01-01 00:00:00", "end": "2024-01-31 00:00:00"}],
    )
    assert result.iloc[0]["remanent"] == 100.0


def test_verification_example():
    df = make_df([
        {"date": "2023-02-28 10:00:00", "amount": 375.0, "ceiling": 400.0, "remanent": 25.0},
        {"date": "2023-07-01 12:00:00", "amount": 620.0, "ceiling": 700.0, "remanent": 80.0},
        {"date": "2023-10-12 14:00:00", "amount": 250.0, "ceiling": 300.0, "remanent": 50.0},
        {"date": "2023-12-17 16:00:00", "amount": 480.0, "ceiling": 500.0, "remanent": 20.0},
    ])
    q = [{"fixed": 0, "start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59"}]
    p = [{"extra": 25, "start": "2023-10-01 00:00:00", "end": "2023-12-31 23:59:59"}]
    result = apply_temporal_rules(df, q, p)
    remanents = result["remanent"].tolist()
    assert remanents[0] == 25.0
    assert remanents[1] == 0.0
    assert remanents[2] == 75.0
    assert remanents[3] == 45.0