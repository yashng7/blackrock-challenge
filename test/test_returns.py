import pytest
from app.engines.returns import years_to_retirement, compute_nps, compute_index


def test_years_under_60():
    assert years_to_retirement(29) == 31
    assert years_to_retirement(30) == 30
    assert years_to_retirement(55) == 5


def test_years_60_plus():
    assert years_to_retirement(60) == 5
    assert years_to_retirement(65) == 5


def test_nps_verification():
    k_results = [{"start": "s", "end": "e", "amount": 145}]
    result = compute_nps(k_results, 29, 0.055)
    assert result[0]["profits"] == pytest.approx(86.88, abs=1.0)


def test_index_verification():
    k_results = [{"start": "s", "end": "e", "amount": 145}]
    result = compute_index(k_results, 29, 0.055)
    assert result[0]["return"] == pytest.approx(1829.5, abs=5.0)


def test_nps_zero_amount():
    k_results = [{"start": "s", "end": "e", "amount": 0}]
    result = compute_nps(k_results, 30, 0.055)
    assert result[0]["profits"] == 0


def test_index_zero_inflation():
    k_results = [{"start": "s", "end": "e", "amount": 100}]
    result = compute_index(k_results, 30, 0)
    fv = 100 * (1.1449 ** 30)
    assert result[0]["return"] == pytest.approx(fv, rel=0.001)