from pathlib import Path


DATA_PATH = Path("data/sample_vending_data.csv")
REPORT_PATH = Path("reports/weekly_decision_report.md")

REQUIRED_COLUMNS = {
    "date",
    "machine_id",
    "location",
    "product_id",
    "product_name",
    "category",
    "price",
    "current_stock",
    "max_capacity",
    "units_sold",
    "last_refill_date",
    "machine_status",
}
