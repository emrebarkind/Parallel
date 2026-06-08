import unittest
from pathlib import Path

from parallel.data import load_vending_data
from parallel.report import analyze_vending_data


class SampleDatasetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = load_vending_data(Path("data/sample_vending_data.csv"))

    def test_sample_dataset_has_multi_day_coverage(self):
        self.assertGreaterEqual(self.df["date"].nunique(), 21)
        self.assertGreaterEqual(self.df["machine_id"].nunique(), 4)
        self.assertLessEqual(self.df["machine_id"].nunique(), 6)
        self.assertGreaterEqual(self.df["product_id"].nunique(), 12)
        self.assertLessEqual(self.df["product_id"].nunique(), 20)

    def test_sample_dataset_includes_operational_edge_cases(self):
        self.assertTrue((self.df["current_stock"] <= 4).any())
        self.assertTrue((self.df["machine_status"] != "OK").any())
        self.assertTrue((self.df["category"] == "Fresh Food").any())

    def test_analysis_summarizes_to_current_product_slots(self):
        analysis_df = analyze_vending_data(self.df)
        product_slots = self.df[["machine_id", "product_id"]].drop_duplicates()

        self.assertEqual(len(analysis_df), len(product_slots))
        self.assertTrue((analysis_df["stockout_risk"] == "High").any())
        self.assertTrue((analysis_df["waste_risk"] == "High").any())
        self.assertTrue((analysis_df["priority"] == "High").any())


if __name__ == "__main__":
    unittest.main()
