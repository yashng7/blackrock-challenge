import pandas as pd
import numpy as np


def parse_expenses(expenses: list[dict]) -> pd.DataFrame:
    if not expenses:
        return pd.DataFrame(columns=["date", "amount", "ceiling", "remanent"])

    df = pd.DataFrame(expenses)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
    amounts = df["amount"].to_numpy(dtype=np.float64)
    ceilings = np.ceil(amounts / 100.0) * 100.0
    df["amount"] = amounts
    df["ceiling"] = ceilings
    df["remanent"] = ceilings - amounts

    return df[["date", "amount", "ceiling", "remanent"]]