from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/sample_vending_data.csv")
REPORT_PATH = Path("reports/weekly_decision_report.md")


def classify_stockout_risk(row):
    units_sold = max(float(row["units_sold"]), 0.1)
    current_stock = float(row["current_stock"])
    days_until_stockout = current_stock / units_sold

    if days_until_stockout < 1:
        return "High", days_until_stockout
    if days_until_stockout <= 3:
        return "Medium", days_until_stockout
    return "Low", days_until_stockout


def classify_waste_risk(row):
    current_stock = float(row["current_stock"])
    max_capacity = max(float(row["max_capacity"]), 1)
    units_sold = float(row["units_sold"])
    stock_ratio = current_stock / max_capacity

    if stock_ratio > 0.70 and units_sold <= 2:
        return "High"
    if stock_ratio > 0.50 and units_sold <= 4:
        return "Medium"
    return "Low"


def build_recommendation(row):
    stockout_risk = row["stockout_risk"]
    waste_risk = row["waste_risk"]

    if stockout_risk == "High":
        return "Restock before the next service window", "Current stock is low compared to recent sales."
    if waste_risk == "High":
        return "Reduce quantity in the next refill cycle", "Current stock is high while recent sales are low."
    if row["machine_status"] != "OK":
        return "Review machine status during the next visit", "Machine status indicates that a service check may be needed."
    if stockout_risk == "Medium":
        return "Monitor and consider restocking soon", "Product may run out within the next few days."
    if waste_risk == "Medium":
        return "Monitor product rotation", "Product is moving slowly compared to available stock."
    return "No immediate action required", "Stock and sales levels look healthy."


def priority_score(row):
    score = 0
    if row["stockout_risk"] == "High":
        score += 3
    elif row["stockout_risk"] == "Medium":
        score += 2

    if row["waste_risk"] == "High":
        score += 2
    elif row["waste_risk"] == "Medium":
        score += 1

    if row["machine_status"] != "OK":
        score += 2

    if score >= 4:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def generate_report():
    df = pd.read_csv(DATA_PATH)

    risk_results = df.apply(classify_stockout_risk, axis=1)
    df["stockout_risk"] = [risk for risk, _ in risk_results]
    df["days_until_stockout"] = [round(days, 1) for _, days in risk_results]
    df["waste_risk"] = df.apply(classify_waste_risk, axis=1)
    df["priority"] = df.apply(priority_score, axis=1)

    recommendations = df.apply(build_recommendation, axis=1)
    df["recommendation"] = [rec for rec, _ in recommendations]
    df["explanation"] = [exp for _, exp in recommendations]

    high_stockout_count = int((df["stockout_risk"] == "High").sum())
    high_waste_count = int((df["waste_risk"] == "High").sum())
    high_priority_count = int((df["priority"] == "High").sum())

    report_lines = [
        "# Weekly Decision Report",
        "",
        "## Executive Summary",
        "",
        f"- Machines analyzed: {df['machine_id'].nunique()}",
        f"- Products analyzed: {len(df)}",
        f"- High stockout risks: {high_stockout_count}",
        f"- High waste risks: {high_waste_count}",
        f"- High priority actions: {high_priority_count}",
        "",
        "## Recommended Actions",
        "",
        "| Priority | Machine | Location | Product | Issue | Recommendation | Explanation |",
        "|---|---|---|---|---|---|---|",
    ]

    sorted_df = df.sort_values(by=["priority", "stockout_risk", "waste_risk"], ascending=True)
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    sorted_df = df.assign(priority_rank=df["priority"].map(priority_order)).sort_values("priority_rank")

    for _, row in sorted_df.iterrows():
        issue = f"Stockout: {row['stockout_risk']} / Waste: {row['waste_risk']}"
        report_lines.append(
            f"| {row['priority']} | {row['machine_id']} | {row['location']} | {row['product_name']} | {issue} | {row['recommendation']} | {row['explanation']} |"
        )

    report_lines.extend([
        "",
        "## Notes",
        "",
        "Recommendations are intended for operator review and approval. The MVP is designed to support human-supervised operational decisions, not to automatically execute changes.",
    ])

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report generated: {REPORT_PATH}")


if __name__ == "__main__":
    generate_report()
