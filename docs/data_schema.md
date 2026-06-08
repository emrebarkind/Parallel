# Data Schema

The MVP uses a simple CSV-based data format. This allows the system to work with simulated, exported, or historical vending machine data before live integrations are available.

## Required Columns

| Column | Description | Example |
|---|---|---|
| date | Date of the observation or sales record | 2026-05-01 |
| machine_id | Unique vending machine identifier | M-001 |
| location | Machine location | Engineering Building |
| product_id | Unique product identifier | P-001 |
| product_name | Product name | Water 500ml |
| category | Product category | Drink |
| price | Product price | 1.20 |
| current_stock | Current product stock in the machine | 6 |
| max_capacity | Maximum product capacity in the machine | 30 |
| units_sold | Units sold in the selected period | 14 |
| last_refill_date | Last known refill date | 2026-04-29 |
| machine_status | Machine operational status | OK |

## Example Row

```csv
date,machine_id,location,product_id,product_name,category,price,current_stock,max_capacity,units_sold,last_refill_date,machine_status
2026-05-01,M-001,Engineering Building,P-001,Water 500ml,Drink,1.20,6,30,14,2026-04-29,OK
```

## Notes

- The current schema is intentionally simple.
- Future versions may add expiry dates, refill quantities, service events, payment data, and telemetry fields.
- The MVP should remain flexible enough to accept different operator export formats after normalization.
