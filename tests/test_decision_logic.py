import unittest

import pandas as pd

from parallel.report import analyze_vending_data


def sample_row(**overrides):
    row = {
        "date": pd.Timestamp("2026-05-01"),
        "machine_id": "M-001",
        "location": "Test Location",
        "product_id": "P-001",
        "product_name": "Water",
        "category": "Drink",
        "price": 1.5,
        "current_stock": 20,
        "max_capacity": 30,
        "units_sold": 4,
        "last_refill_date": pd.Timestamp("2026-04-29"),
        "machine_status": "OK",
    }
    row.update(overrides)
    return row


class DecisionLogicTest(unittest.TestCase):
    def analyze_one(self, **overrides):
        return analyze_vending_data(pd.DataFrame([sample_row(**overrides)])).iloc[0]

    def test_high_stockout_becomes_high_priority(self):
        row = self.analyze_one(current_stock=3, units_sold=15)

        self.assertEqual(row["stockout_risk"], "High")
        self.assertEqual(row["priority"], "High")
        self.assertEqual(row["recommendation"], "Restock before the next service window")

    def test_slow_fresh_food_becomes_high_waste_risk(self):
        row = self.analyze_one(
            category="Fresh Food",
            current_stock=14,
            max_capacity=16,
            units_sold=1,
            price=3.8,
        )

        self.assertEqual(row["waste_risk"], "High")
        self.assertEqual(row["priority"], "High")
        self.assertEqual(row["recommendation"], "Reduce refill quantity or rotate assortment")

    def test_machine_status_takes_recommendation_precedence(self):
        row = self.analyze_one(machine_status="SERVICE_CHECK", current_stock=2, units_sold=10)

        self.assertEqual(row["priority"], "High")
        self.assertEqual(row["recommendation"], "Inspect machine before changing product plan")


if __name__ == "__main__":
    unittest.main()
