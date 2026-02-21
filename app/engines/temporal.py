import pandas as pd
import numpy as np


def apply_temporal_rules(df: pd.DataFrame, q_periods: list[dict], p_periods: list[dict]) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    result = df.copy()
    n = len(result)
    dates = result["date"].values.astype("datetime64[ns]")
    remanent = result["remanent"].values.astype(np.float64).copy()

    if q_periods:
        q_df = pd.DataFrame(q_periods)
        q_starts = pd.to_datetime(q_df["start"]).values.astype("datetime64[ns]")
        q_ends = pd.to_datetime(q_df["end"]).values.astype("datetime64[ns]")
        q_fixed = q_df["fixed"].values.astype(np.float64)
        q_order = np.arange(len(q_df), dtype=np.int64)

        dates_col = dates[:, np.newaxis]
        in_range = (dates_col >= q_starts) & (dates_col <= q_ends)

        has_match = in_range.any(axis=1)
        match_indices = np.where(has_match)[0]

        for i in match_indices:
            matched = np.where(in_range[i])[0]
            matched_starts = q_starts[matched]
            latest = matched_starts.max()
            latest_mask = matched_starts == latest
            candidates = matched[latest_mask]
            winner = candidates[np.argmin(q_order[candidates])]
            remanent[i] = q_fixed[winner]

    if p_periods:
        p_df = pd.DataFrame(p_periods)
        p_starts = pd.to_datetime(p_df["start"]).values.astype("datetime64[ns]")
        p_ends = pd.to_datetime(p_df["end"]).values.astype("datetime64[ns]")
        p_extras = p_df["extra"].values.astype(np.float64)

        dates_col = dates[:, np.newaxis]
        in_range = (dates_col >= p_starts) & (dates_col <= p_ends)
        remanent += (in_range * p_extras).sum(axis=1)

    result["remanent"] = remanent
    return result[["date", "amount", "ceiling", "remanent"]]