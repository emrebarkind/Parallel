# Parallel Vending Intelligence

**Parallel is an open-source decision engine for vending operations.**

Parallel transforms vending machine sales, stock, refill, product, and machine-status data into weekly operational recommendations that help operators reduce stockouts, lower waste, improve service efficiency, and grow revenue.

## Problem

Vending machines generate operational data every day, but that data often does not turn into timely decisions. Operators still need to decide manually which machines need attention, which products are at risk of running out, which products are moving slowly, and where service visits should be prioritized.

Parallel starts from a simple insight:

> The data exists. The decisions do not follow.

## MVP Scope

The first MVP focuses on a simple workflow:

1. Import vending data from CSV
2. Detect stockout and waste risks
3. Prioritize machines for service
4. Generate a Weekly Decision Report
5. Collect operator feedback for future improvement

The first version does **not** require live telemetry or direct vending machine integration. It works with sample, exported, or historical vending data.

## Current Workflow

```text
sample_vending_data.csv -> analysis -> recommendations -> weekly_decision_report.md
```

<<<<<<< HEAD
The sample dataset includes 28 days of daily product-slot records across 5 machines and 15 products. The report engine summarizes those records into one current decision row per machine/product using the latest stock state and recent sales velocity.

=======
>>>>>>> fd15a1febe40fb5cdee277fb0fb48ed8fba6444e
## Project Structure

```text
generate_report.py        # Small demo entry point
parallel/
  config.py               # MVP paths and required CSV columns
  data.py                 # CSV loading and validation
  risk.py                 # Stockout, waste, and operating metrics
  recommendations.py      # Service priority and action logic
  report.py               # Analysis orchestration and Markdown output
```

The package is intentionally small so operators and contributors can understand the decision logic without navigating a large framework.

## Example Recommendations

- Restock high-demand products before the next service window
- Reduce quantity for slow-moving products
- Prioritize machines with high stockout or service risk
- Skip machines with healthy stock levels
- Review product assortment opportunities

## Running the Demo

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate a sample report:

```bash
python3 generate_report.py
```

The generated report will be available at:

```text
reports/weekly_decision_report.md
```

## Roadmap

### v0.1 — Data to Report

- CSV import
- Stockout risk calculation
- Slow mover / waste risk calculation
- Basic service priority score
- Markdown Weekly Decision Report

### v0.2 — Recommendation Engine

- Structured recommendation logic
- Better explanation text
- Category and product-level performance analysis
- HTML report export

### v0.3 — Operator Feedback

- Approve / reject / edit recommendation status
- Recommendation history
- Feedback log
- Outcome tracking

### v0.4 — Dashboard

- Simple web interface
- Machine overview
- Risk cards
- Weekly report preview

### v0.5 — API Ready

- FastAPI backend
- Upload endpoint
- Recommendation endpoint
- Integration-ready architecture

## License

This project is released under the MIT License.
