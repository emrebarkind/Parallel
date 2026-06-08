import pandas as pd


FRESH_CATEGORIES = {"fresh food", "fresh", "sandwich", "meal"}


def risk_label(score: int) -> str:
    if score >= 3:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def add_operating_metrics(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    days_since_refill = (result["date"] - result["last_refill_date"]).dt.days
    result["days_since_refill"] = days_since_refill.fillna(7).clip(lower=1)
    velocity_days = result.get("observation_days", result["days_since_refill"]).clip(lower=1)
    result["sales_velocity"] = result["units_sold"].clip(lower=0) / velocity_days

    result["stock_fill_ratio"] = (
        result["current_stock"].clip(lower=0) / result["max_capacity"].clip(lower=1)
    ).clip(upper=1)
    result["sell_through_ratio"] = (
        result["units_sold"].clip(lower=0)
        / (result["units_sold"].clip(lower=0) + result["current_stock"].clip(lower=0)).clip(lower=1)
    )

    result["days_until_stockout"] = result.apply(_days_until_stockout, axis=1)
    return result


def classify_stockout_risk(row: pd.Series) -> tuple[str, int]:
    days_until_stockout = float(row["days_until_stockout"])
    sell_through_ratio = float(row["sell_through_ratio"])
    stock_fill_ratio = float(row["stock_fill_ratio"])

    score = 0
    if days_until_stockout <= 2:
        score += 3
    elif days_until_stockout <= 5:
        score += 2
    elif days_until_stockout <= 8:
        score += 1

    if sell_through_ratio >= 0.75:
        score += 1
    if stock_fill_ratio <= 0.15:
        score += 1

    return risk_label(score), score


def classify_waste_risk(row: pd.Series) -> tuple[str, int]:
    category = str(row["category"]).strip().lower()
    is_fresh = category in FRESH_CATEGORIES
    stock_fill_ratio = float(row["stock_fill_ratio"])
    sales_velocity = float(row["sales_velocity"])
    sell_through_ratio = float(row["sell_through_ratio"])

    score = 0
    if stock_fill_ratio >= 0.75 and sales_velocity <= 1.0:
        score += 3
    elif stock_fill_ratio >= 0.55 and sales_velocity <= 2.0:
        score += 2
    elif stock_fill_ratio >= 0.45 and sales_velocity <= 3.0:
        score += 1

    if sell_through_ratio <= 0.15 and stock_fill_ratio >= 0.5:
        score += 1
    if is_fresh and stock_fill_ratio >= 0.5 and sales_velocity <= 2.0:
        score += 1

    return risk_label(score), score


def add_risk_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = add_operating_metrics(df)

    stockout_results = result.apply(classify_stockout_risk, axis=1)
    result["stockout_risk"] = [label for label, _ in stockout_results]
    result["stockout_score"] = [score for _, score in stockout_results]
    result["days_until_stockout"] = result["days_until_stockout"].round(1)

    waste_results = result.apply(classify_waste_risk, axis=1)
    result["waste_risk"] = [label for label, _ in waste_results]
    result["waste_score"] = [score for _, score in waste_results]

    return result


def _days_until_stockout(row: pd.Series) -> float:
    sales_velocity = float(row["sales_velocity"])
    current_stock = max(float(row["current_stock"]), 0)
    if sales_velocity <= 0:
        return 999.0
    return current_stock / sales_velocity
