from fastapi import APIRouter, HTTPException
from app.models.schemas import FilterRequest, FilterResponse, FilterTransactionOut, InvalidTransaction
from app.engines.temporal import apply_temporal_rules
from app.engines.validator import validate_transactions
import pandas as pd

router = APIRouter(prefix="/blackrock/challenge/v1")


@router.post("/transactions:filter", response_model=FilterResponse)
def transactions_filter(req: FilterRequest):
    try:
        if not req.transactions:
            return FilterResponse(valid=[], invalid=[])

        records = [
            {"date": t.date, "amount": t.amount, "ceiling": t.ceiling, "remanent": t.remanent}
            for t in req.transactions
        ]
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
        df["amount"] = df["amount"].astype(float)
        df["ceiling"] = df["ceiling"].astype(float)
        df["remanent"] = df["remanent"].astype(float)

        valid_df, invalid_list = validate_transactions(df)

        invalid_out = [
            InvalidTransaction(
                date=e["date"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(e["date"], "strftime") else str(e["date"]),
                amount=float(e["amount"]),
                ceiling=float(e["ceiling"]),
                remanent=float(e["remanent"]),
                message=e["message"],
            )
            for e in invalid_list
        ]

        if valid_df.empty:
            return FilterResponse(valid=[], invalid=invalid_out)

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

        result_df = apply_temporal_rules(valid_df, valid_q, valid_p)

        in_any_k = pd.Series(False, index=result_df.index)
        if req.k:
            dates = result_df["date"].values.astype("datetime64[ns]")
            for kp in req.k:
                k_start = pd.to_datetime(kp.start)
                k_end = pd.to_datetime(kp.end)
                if k_start.year == k_end.year and k_start <= k_end:
                    in_any_k |= pd.Series(
                        (dates >= k_start.to_datetime64()) & (dates <= k_end.to_datetime64()),
                        index=result_df.index,
                    )

        valid_out = [
            FilterTransactionOut(
                date=row["date"].strftime("%Y-%m-%d %H:%M:%S"),
                amount=row["amount"],
                ceiling=row["ceiling"],
                remanent=row["remanent"],
                inKPeriod=bool(in_any_k.iloc[i]),
            )
            for i, (_, row) in enumerate(result_df.iterrows())
        ]

        return FilterResponse(valid=valid_out, invalid=invalid_out)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))