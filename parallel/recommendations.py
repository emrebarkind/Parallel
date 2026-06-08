import pandas as pd


def add_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    priority_results = result.apply(classify_service_priority, axis=1)
    result["priority"] = [label for label, _ in priority_results]
    result["priority_score"] = [score for _, score in priority_results]

    recommendation_results = result.apply(build_recommendation, axis=1)
    result["recommendation"] = [recommendation for recommendation, _ in recommendation_results]
    result["explanation"] = [explanation for _, explanation in recommendation_results]
    return result


def classify_service_priority(row: pd.Series) -> tuple[str, int]:
    score = int(row["stockout_score"]) + int(row["waste_score"])

    if row["machine_status"] not in {"OK", "ONLINE"}:
        score += 3
    if row["stockout_risk"] == "High" and row["waste_risk"] == "High":
        score += 1
    if row["stockout_risk"] == "High" or row["waste_risk"] == "High":
        score = max(score, 4)
    if float(row["price"]) >= 3 and row["stockout_risk"] in {"High", "Medium"}:
        score += 1

    if score >= 4:
        return "High", score
    if score >= 2:
        return "Medium", score
    return "Low", score


def build_recommendation(row: pd.Series) -> tuple[str, str]:
    if row["machine_status"] not in {"OK", "ONLINE"}:
        return (
            "Inspect machine before changing product plan",
            f"Machine status is {row['machine_status']}, so service reliability should be checked first.",
        )

    if row["stockout_risk"] == "High":
        return (
            "Restock before the next service window",
            f"At the current sales pace, available stock may last about {row['days_until_stockout']} day(s).",
        )

    if row["waste_risk"] == "High":
        return (
            "Reduce refill quantity or rotate assortment",
            "Stock is high relative to recent movement, increasing slow-mover or spoilage risk.",
        )

    if row["stockout_risk"] == "Medium":
        return (
            "Add to the next refill route",
            f"Demand is steady and stock may run out in about {row['days_until_stockout']} day(s).",
        )

    if row["waste_risk"] == "Medium":
        return (
            "Refill conservatively and monitor rotation",
            "Current inventory is above demand, but the product does not need urgent action.",
        )

    if float(row["sales_velocity"]) <= 0:
        return (
            "Review product placement",
            "No recent sales were recorded, so this slot may need operator review.",
        )

    return (
        "No immediate action required",
        "Stock level, sales pace, and machine status look healthy.",
    )
