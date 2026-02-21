import pytest
from app.engines.tax import compute_tax, compute_deduction, apply_tax_benefit


def test_tax_below_7l():
    assert compute_tax(500000) == 0
    assert compute_tax(600000) == 0
    assert compute_tax(700000) == 0


def test_tax_first_slab():
    assert compute_tax(800000) == 10000
    assert compute_tax(1000000) == 30000


def test_tax_second_slab():
    assert compute_tax(1200000) == 60000


def test_tax_top_slab():
    assert compute_tax(1800000) == 210000


def test_deduction_cap():
    assert compute_deduction(100, 2000000) == 100
    assert compute_deduction(500000, 1000000) == 100000
    assert compute_deduction(500000, 5000000) == 200000


def test_tax_benefit_below_threshold():
    nps = [{"start": "s", "end": "e", "amount": 1000, "profits": 50}]
    result = apply_tax_benefit(nps, 600000)
    assert result[0]["taxBenefit"] == 0


def test_tax_benefit_high_income():
    nps = [{"start": "s", "end": "e", "amount": 50000, "profits": 100}]
    result = apply_tax_benefit(nps, 1800000)
    assert result[0]["taxBenefit"] == 15000