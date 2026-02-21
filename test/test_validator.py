import pytest
import pandas as pd
from app.engines.validator import validate_transactions


def test_valid_transaction():
    df = pd.DataFrame([{
        "date": pd.to_datetime("2024-01-15 10:30:00"),
        "amount": 250.0, "ceiling": 300.0, "remanent": 50.0,
    }])
    valid, invalid = validate_transactions(df)
    assert len(valid) == 1
    assert len(invalid) == 0


def test_zero_amount_valid():
    df = pd.DataFrame([{
        "date": pd.to_datetime("2024-01-15 10:30:00"),
        "amount": 0.0, "ceiling": 0.0, "remanent": 0.0,
    }])
    valid, invalid = validate_transactions(df)
    assert len(valid) == 1
    assert len(invalid) == 0


def test_negative_amount():
    df = pd.DataFrame([{
        "date": pd.to_datetime("2024-01-15 10:30:00"),
        "amount": -5.0, "ceiling": 100.0, "remanent": 105.0,
    }])
    valid, invalid = validate_transactions(df)
    assert len(valid) == 0
    assert invalid[0]["message"] == "Negative amounts are not allowed"


def test_wrong_ceiling():
    df = pd.DataFrame([{
        "date": pd.to_datetime("2024-01-15 10:30:00"),
        "amount": 250.0, "ceiling": 999.0, "remanent": 749.0,
    }])
    valid, invalid = validate_transactions(df)
    assert len(valid) == 0
    assert invalid[0]["message"] == "Invalid or missing fields"


def test_duplicate_timestamp():
    df = pd.DataFrame([
        {"date": pd.to_datetime("2024-01-15 10:30:00"), "amount": 250.0, "ceiling": 300.0, "remanent": 50.0},
        {"date": pd.to_datetime("2024-01-15 10:30:00"), "amount": 100.0, "ceiling": 100.0, "remanent": 0.0},
    ])
    valid, invalid = validate_transactions(df)
    assert len(valid) == 0
    assert len(invalid) == 2
    assert all(i["message"] == "Duplicate transaction" for i in invalid)


def test_empty_dataframe():
    df = pd.DataFrame(columns=["date", "amount", "ceiling", "remanent"])
    valid, invalid = validate_transactions(df)
    assert len(valid) == 0
    assert len(invalid) == 0