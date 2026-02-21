from fastapi import APIRouter, HTTPException
from app.models.schemas import ValidatorRequest, ValidatorResponse, TransactionOut, InvalidTransaction
from app.engines.validator import validate_transactions
import pandas as pd

router = APIRouter(prefix="/blackrock/challenge/v1")


@router.post("/transactions:validator", response_model=ValidatorResponse)
def transactions_validator(req: ValidatorRequest):
    try:
        records = [
            {"date": t.date, "amount": t.amount, "ceiling": t.ceiling, "remanent": t.remanent}
            for t in req.transactions
        ]

        if not records:
            return ValidatorResponse(valid=[], invalid=[])

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
        df["amount"] = df["amount"].astype(float)
        df["ceiling"] = df["ceiling"].astype(float)
        df["remanent"] = df["remanent"].astype(float)

        valid_df, invalid_list = validate_transactions(df)

        valid_out = [
            TransactionOut(
                date=row["date"].strftime("%Y-%m-%d %H:%M:%S"),
                amount=row["amount"],
                ceiling=row["ceiling"],
                remanent=row["remanent"],
            )
            for _, row in valid_df.iterrows()
        ]

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

        return ValidatorResponse(valid=valid_out, invalid=invalid_out)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))