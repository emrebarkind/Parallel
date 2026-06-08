from pathlib import Path

import pandas as pd

from .config import REQUIRED_COLUMNS


def load_vending_data(path: Path) -> pd.DataFrame:
    """Load and validate the MVP vending CSV."""
    df = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    numeric_columns = ["price", "current_stock", "max_capacity", "units_sold"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["last_refill_date"] = pd.to_datetime(df["last_refill_date"], errors="coerce")
    df["machine_status"] = df["machine_status"].fillna("UNKNOWN").astype(str).str.upper()
    df["category"] = df["category"].fillna("Unknown")

<<<<<<< HEAD
    return df.sort_values(["date", "machine_id", "product_id"]).reset_index(drop=True)


def prepare_analysis_data(df: pd.DataFrame, lookback_days: int = 7) -> pd.DataFrame:
    """Build one current decision row per machine/product from multi-day records."""
    if df.empty:
        return df.copy()

    group_columns = ["machine_id", "product_id"]
    latest_date = df["date"].max()
    window_start = latest_date - pd.Timedelta(days=lookback_days - 1)
    recent_df = df[df["date"] >= window_start]

    latest_rows = (
        df.sort_values(["date", "machine_id", "product_id"])
        .groupby(group_columns, as_index=False)
        .tail(1)
        .drop(columns=["units_sold"])
    )

    recent_sales = (
        recent_df.groupby(group_columns, as_index=False)
        .agg(units_sold=("units_sold", "sum"), observation_days=("date", "nunique"))
    )

    analysis_df = latest_rows.merge(recent_sales, on=group_columns, how="left")
    analysis_df["units_sold"] = analysis_df["units_sold"].fillna(0)
    analysis_df["observation_days"] = analysis_df["observation_days"].fillna(1)
    return analysis_df.sort_values(group_columns).reset_index(drop=True)
=======
    return df
>>>>>>> fd15a1febe40fb5cdee277fb0fb48ed8fba6444e
