import pandas as pd
import numpy as np


def validate_transactions(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    if df.empty:
        return df.copy(), []

    invalid = []
    valid_mask = np.ones(len(df), dtype=bool)

    required = ["date", "amount", "ceiling", "remanent"]
    for col in required:
        if col not in df.columns:
            for _, row in df.iterrows():
                invalid.append({**row.to_dict(), "message": "Invalid or missing fields"})
            return pd.DataFrame(columns=required), invalid

    amounts = pd.to_numeric(df["amount"], errors="coerce")
    ceilings = pd.to_numeric(df["ceiling"], errors="coerce")
    remanents = pd.to_numeric(df["remanent"], errors="coerce")
    non_finite = amounts.isna() | ceilings.isna() | remanents.isna()

    if non_finite.any():
        idxs = df.index[non_finite & valid_mask]
        for idx in idxs:
            invalid.append({**df.loc[idx].to_dict(), "message": "Invalid or missing fields"})
        valid_mask &= ~non_finite.to_numpy()

    amounts_np = amounts.to_numpy(dtype=np.float64)
    negative = amounts_np < 0
    if negative.any():
        idxs = df.index[negative & valid_mask]
        for idx in idxs:
            invalid.append({**df.loc[idx].to_dict(), "message": "Negative amounts are not allowed"})
        valid_mask &= ~negative

    expected_ceiling = np.ceil(amounts_np / 100.0) * 100.0
    ceiling_mismatch = ~np.isclose(ceilings.to_numpy(), expected_ceiling, rtol=1e-9)
    if ceiling_mismatch.any():
        idxs = df.index[ceiling_mismatch & valid_mask]
        for idx in idxs:
            invalid.append({**df.loc[idx].to_dict(), "message": "Invalid or missing fields"})
        valid_mask &= ~ceiling_mismatch

    expected_remanent = ceilings.to_numpy() - amounts_np
    remanent_mismatch = ~np.isclose(remanents.to_numpy(), expected_remanent, rtol=1e-9)
    if remanent_mismatch.any():
        idxs = df.index[remanent_mismatch & valid_mask]
        for idx in idxs:
            invalid.append({**df.loc[idx].to_dict(), "message": "Invalid or missing fields"})
        valid_mask &= ~remanent_mismatch

    date_series = df["date"]
    duplicated = date_series.duplicated(keep=False).to_numpy()
    if duplicated.any():
        idxs = df.index[duplicated & valid_mask]
        for idx in idxs:
            invalid.append({**df.loc[idx].to_dict(), "message": "Duplicate transaction"})
        valid_mask &= ~duplicated

    valid_df = df.loc[valid_mask].copy().reset_index(drop=True)
    return valid_df, invalid