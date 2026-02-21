SLABS = [
    (700000, 1000000, 0.10),
    (1000000, 1200000, 0.15),
    (1200000, 1500000, 0.20),
    (1500000, float("inf"), 0.30),
]


def compute_tax(income: float) -> float:
    if income <= 700000:
        return 0.0
    tax = 0.0
    for lower, upper, rate in SLABS:
        if income <= lower:
            break
        tax += (min(income, upper) - lower) * rate
    return tax


def compute_deduction(amount: float, annual_income: float) -> float:
    return min(amount, 0.1 * annual_income, 200000.0)


def apply_tax_benefit(nps_results: list[dict], annual_income: float) -> list[dict]:
    base_tax = compute_tax(annual_income)
    output = []

    for entry in nps_results:
        deduction = compute_deduction(entry["amount"], annual_income)
        reduced_tax = compute_tax(annual_income - deduction)
        output.append({
            "start": entry["start"],
            "end": entry["end"],
            "amount": entry["amount"],
            "profits": entry["profits"],
            "taxBenefit": base_tax - reduced_tax,
        })

    return output