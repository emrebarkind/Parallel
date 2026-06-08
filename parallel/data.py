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

    return df
