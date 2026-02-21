import pytest
import pandas as pd
from app.engines.grouping import group_by_k


def test_verification_example():
    df = pd.DataFrame([
        {"date": pd.to_datetime("2023-02-28 10:00:00"), "amount": 375.0, "ceiling": 400.0, "remanent": 25.0},
        {"date": pd.to_datetime("2023-07-01 12:00:00"), "amount": 620.0, "ceiling": 700.0, "remanent": 0.0},
        {"date": pd.to_datetime("2023-10-12 14:00:00"), "amount": 250.0, "ceiling": 300.0, "remanent": 75.0},
        {"date": pd.to_datetime("2023-12-17 16:00:00"), "amount": 480.0, "ceiling": 500.0, "remanent": 45.0},
    ])
    k_periods = [
        {"start": "2023-03-01 00:00:00", "end": "2023-11-30 23:59:59"},
        {"start": "2023-01-01 00:00:00", "end": "2023-12-31 23:59:59"},
    ]
    result = group_by_k(df, k_periods)
    assert result[0]["amount"] == 75.0
    assert result[1]["amount"] == 145.0


def test_multi_k_membership():
    df = pd.DataFrame([
        {"date": pd.to_datetime("2024-01-15 10:30:00"), "amount": 250.0, "ceiling": 300.0, "remanent": 100.0},
        {"date": pd.to_datetime("2024-01-20 14:00:00"), "amount": 180.0, "ceiling": 200.0, "remanent": 125.0},
    ])
    k_periods = [
        {"start": "2024-01-01 00:00:00", "end": "2024-01-31 00:00:00"},
        {"start": "2024-01-18 00:00:00", "end": "2024-01-25 00:00:00"},
    ]
    result = group_by_k(df, k_periods)
    assert result[0]["amount"] == 225.0
    assert result[1]["amount"] == 125.0


def test_empty_k():
    df = pd.DataFrame([
        {"date": pd.to_datetime("2024-01-15 10:30:00"), "amount": 250.0, "ceiling": 300.0, "remanent": 100.0},
    ])
    result = group_by_k(df, [{"start": "2024-02-01 00:00:00", "end": "2024-02-28 00:00:00"}])
    assert result[0]["amount"] == 0.0


def test_no_k():
    result = group_by_k(pd.DataFrame(), [])
    assert len(result) == 0