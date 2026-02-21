import pytest
from app.engines.parser import parse_expenses


def test_basic_rounding():
    expenses = [{"date": "2024-01-15 10:30:00", "amount": 250}]
    df = parse_expenses(expenses)
    assert df.iloc[0]["ceiling"] == 300.0
    assert df.iloc[0]["remanent"] == 50.0


def test_exact_multiple_of_100():
    expenses = [{"date": "2024-01-15 10:30:00", "amount": 200}]
    df = parse_expenses(expenses)
    assert df.iloc[0]["ceiling"] == 200.0
    assert df.iloc[0]["remanent"] == 0.0


def test_small_amount():
    expenses = [{"date": "2024-01-15 10:30:00", "amount": 0.50}]
    df = parse_expenses(expenses)
    assert df.iloc[0]["ceiling"] == 100.0
    assert df.iloc[0]["remanent"] == pytest.approx(99.50)


def test_large_amount():
    expenses = [{"date": "2024-01-15 10:30:00", "amount": 499999.99}]
    df = parse_expenses(expenses)
    assert df.iloc[0]["ceiling"] == 500000.0
    assert df.iloc[0]["remanent"] == pytest.approx(0.01)


def test_empty_expenses():
    df = parse_expenses([])
    assert df.empty


def test_verification_examples():
    expenses = [
        {"date": "2023-10-12 14:00:00", "amount": 250},
        {"date": "2023-02-28 10:00:00", "amount": 375},
        {"date": "2023-07-01 12:00:00", "amount": 620},
        {"date": "2023-12-17 16:00:00", "amount": 480},
    ]
    df = parse_expenses(expenses)
    amounts = dict(zip(df["amount"], df["remanent"]))
    assert amounts[250] == 50
    assert amounts[375] == 25
    assert amounts[620] == 80
    assert amounts[480] == 20