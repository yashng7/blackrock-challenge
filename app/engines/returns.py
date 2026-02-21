import numpy as np

NPS_RATE = 0.0711
INDEX_RATE = 0.1449


def years_to_retirement(age: float) -> int:
    if age < 60:
        return 60 - int(age)
    return 5


def compute_nps(k_results: list[dict], age: float, inflation: float) -> list[dict]:
    t = years_to_retirement(age)
    growth = (1 + NPS_RATE) ** t
    deflator = (1 + inflation) ** t
    output = []

    for k in k_results:
        p = k["amount"]
        real_value = (p * growth) / deflator
        output.append({
            "start": k["start"],
            "end": k["end"],
            "amount": p,
            "profits": real_value - p,
        })

    return output


def compute_index(k_results: list[dict], age: float, inflation: float) -> list[dict]:
    t = years_to_retirement(age)
    growth = (1 + INDEX_RATE) ** t
    deflator = (1 + inflation) ** t
    output = []

    for k in k_results:
        p = k["amount"]
        real_value = (p * growth) / deflator
        output.append({
            "start": k["start"],
            "end": k["end"],
            "amount": p,
            "return": real_value,
        })

    return output