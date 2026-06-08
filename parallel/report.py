from pathlib import Path

import pandas as pd

from .config import DATA_PATH, REPORT_PATH
from .data import load_vending_data, prepare_analysis_data
from .recommendations import add_recommendations
from .risk import add_risk_columns


PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
RISK_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def analyze_vending_data(df: pd.DataFrame) -> pd.DataFrame:
    return add_recommendations(add_risk_columns(prepare_analysis_data(df)))


def generate_report(
    data_path: Path = DATA_PATH,
    report_path: Path = REPORT_PATH,
) -> Path:
    df = analyze_vending_data(load_vending_data(data_path))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_markdown_report(df), encoding="utf-8")
    print(f"Report generated: {report_path}")
    return report_path


def build_markdown_report(df: pd.DataFrame) -> str:
    high_stockout_count = int((df["stockout_risk"] == "High").sum())
    high_waste_count = int((df["waste_risk"] == "High").sum())
    high_priority_count = int((df["priority"] == "High").sum())

    report_lines = [
        "# Weekly Decision Report",
        "",
        "## Executive Summary",
        "",
        f"- Machines analyzed: {df['machine_id'].nunique()}",
        f"- Product slots analyzed: {len(df)}",
        f"- High stockout risks: {high_stockout_count}",
        f"- High waste risks: {high_waste_count}",
        f"- High priority actions: {high_priority_count}",
        "",
        "## Recommended Actions",
        "",
        "| Priority | Machine | Location | Product | Issue | Recommendation | Explanation |",
        "|---|---|---|---|---|---|---|",
    ]

    sorted_df = _sort_for_report(df)
    for _, row in sorted_df.iterrows():
        issue = (
            f"Stockout: {row['stockout_risk']} "
            f"({row['days_until_stockout']} days) / Waste: {row['waste_risk']}"
        )
        report_lines.append(
            "| "
            f"{row['priority']} | "
            f"{row['machine_id']} | "
            f"{row['location']} | "
            f"{row['product_name']} | "
            f"{issue} | "
            f"{row['recommendation']} | "
            f"{row['explanation']} |"
        )

    report_lines.extend(
        [
            "",
            "## Notes",
            "",
            "Recommendations are intended for operator review and approval. The MVP is designed to support human-supervised operational decisions, not to automatically execute changes.",
        ]
    )

    return "\n".join(report_lines)


def _sort_for_report(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(
            priority_rank=df["priority"].map(PRIORITY_ORDER),
            stockout_rank=df["stockout_risk"].map(RISK_ORDER),
            waste_rank=df["waste_risk"].map(RISK_ORDER),
        )
        .sort_values(
            by=[
                "priority_rank",
                "priority_score",
                "stockout_rank",
                "waste_rank",
                "machine_id",
                "product_name",
            ],
            ascending=[True, False, True, True, True, True],
        )
        .drop(columns=["priority_rank", "stockout_rank", "waste_rank"])
    )
