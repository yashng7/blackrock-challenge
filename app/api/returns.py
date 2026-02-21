from fastapi import APIRouter, HTTPException
from app.models.schemas import ReturnsRequest, NPSResponse, NPSSavings, IndexResponse, IndexSavings
from app.engines.parser import parse_expenses
from app.engines.validator import validate_transactions
from app.engines.temporal import apply_temporal_rules
from app.engines.grouping import group_by_k
from app.engines.returns import compute_nps, compute_index
from app.engines.tax import apply_tax_benefit
import pandas as pd

router = APIRouter(prefix="/blackrock/challenge/v1")


def run_pipeline(req: ReturnsRequest):
    if not req.transactions:
        return None, 0.0, 0.0, []

    raw = [{"date": t.date, "amount": t.amount} for t in req.transactions]
    parsed_df = parse_expenses(raw)
    valid_df, _ = validate_transactions(parsed_df)

    total_amount = float(valid_df["amount"].sum()) if not valid_df.empty else 0.0
    total_ceiling = float(valid_df["ceiling"].sum()) if not valid_df.empty else 0.0

    if valid_df.empty:
        return valid_df, total_amount, total_ceiling, []

    valid_q = [
        {"fixed": qp.fixed, "start": qp.start, "end": qp.end}
        for qp in req.q
        if pd.to_datetime(qp.start) <= pd.to_datetime(qp.end) and qp.fixed < 500000
    ]

    valid_p = [
        {"extra": pp.extra, "start": pp.start, "end": pp.end}
        for pp in req.p
        if pd.to_datetime(pp.start) <= pd.to_datetime(pp.end) and pp.extra < 500000
    ]

    temporal_df = apply_temporal_rules(valid_df, valid_q, valid_p)

    valid_k = [
        {"start": kp.start, "end": kp.end}
        for kp in req.k
        if pd.to_datetime(kp.start).year == pd.to_datetime(kp.end).year
        and pd.to_datetime(kp.start) <= pd.to_datetime(kp.end)
    ]

    k_results = group_by_k(temporal_df, valid_k)
    return temporal_df, total_amount, total_ceiling, k_results


@router.post("/returns:nps", response_model=NPSResponse)
def returns_nps(req: ReturnsRequest):
    try:
        _, total_amount, total_ceiling, k_results = run_pipeline(req)
        annual_income = req.wage * 12
        inflation = req.inflation / 100

        if not k_results:
            return NPSResponse(totalTransactionAmount=total_amount, totalCeiling=total_ceiling, savingsByDates=[])

        nps_results = compute_nps(k_results, req.age, inflation)
        nps_with_tax = apply_tax_benefit(nps_results, annual_income)

        savings = [
            NPSSavings(start=r["start"], end=r["end"], amount=r["amount"], profit=r["profits"], taxBenefit=r["taxBenefit"])
            for r in nps_with_tax
        ]

        return NPSResponse(totalTransactionAmount=total_amount, totalCeiling=total_ceiling, savingsByDates=savings)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/returns:index", response_model=IndexResponse)
def returns_index(req: ReturnsRequest):
    try:
        _, total_amount, total_ceiling, k_results = run_pipeline(req)
        inflation = req.inflation / 100

        if not k_results:
            return IndexResponse(totalTransactionAmount=total_amount, totalCeiling=total_ceiling, savingsByDates=[])

        index_results = compute_index(k_results, req.age, inflation)

        savings = [
            IndexSavings(start=r["start"], end=r["end"], amount=r["amount"], return_=r["return"])
            for r in index_results
        ]

        return IndexResponse(totalTransactionAmount=total_amount, totalCeiling=total_ceiling, savingsByDates=savings)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))