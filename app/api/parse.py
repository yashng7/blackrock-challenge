from fastapi import APIRouter, HTTPException
from app.models.schemas import ParseRequest, ParseResponse, TransactionOut
from app.engines.parser import parse_expenses

router = APIRouter(prefix="/blackrock/challenge/v1")


@router.post("/transactions:parse", response_model=ParseResponse)
def transactions_parse(req: ParseRequest):
    try:
        raw = [{"date": e.date, "amount": e.amount} for e in req.expenses]
        df = parse_expenses(raw)

        transactions = [
            TransactionOut(
                date=row["date"].strftime("%Y-%m-%d %H:%M:%S"),
                amount=row["amount"],
                ceiling=row["ceiling"],
                remanent=row["remanent"],
            )
            for _, row in df.iterrows()
        ]

        return ParseResponse(
            transactions=transactions,
            totalAmount=float(df["amount"].sum()) if not df.empty else 0.0,
            totalCeiling=float(df["ceiling"].sum()) if not df.empty else 0.0,
            totalRemanent=float(df["remanent"].sum()) if not df.empty else 0.0,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))