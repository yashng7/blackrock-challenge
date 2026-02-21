import pandas as pd
import numpy as np


def group_by_k(df: pd.DataFrame, k_periods: list[dict]) -> list[dict]:
    if not k_periods:
        return []

    if df.empty:
        return [{"start": kp["start"], "end": kp["end"], "amount": 0.0} for kp in k_periods]

    dates = df["date"].values.astype("datetime64[ns]")
    remanents = df["remanent"].values.astype(np.float64)
    results = []

    for kp in k_periods:
        k_start = np.datetime64(pd.to_datetime(kp["start"]))
        k_end = np.datetime64(pd.to_datetime(kp["end"]))
        mask = (dates >= k_start) & (dates <= k_end)
        amount = float(remanents[mask].sum())
        results.append({"start": kp["start"], "end": kp["end"], "amount": amount})

    return results