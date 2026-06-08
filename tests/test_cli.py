import unittest
from pathlib import Path
from unittest.mock import patch

import generate_report
from parallel.config import DATA_PATH, REPORT_PATH


class CliTest(unittest.TestCase):
    def test_parse_args_uses_default_paths(self):
        with patch("sys.argv", ["generate_report.py"]):
            args = generate_report.parse_args()

        self.assertEqual(args.input, DATA_PATH)
        self.assertEqual(args.output, REPORT_PATH)

    def test_parse_args_accepts_custom_paths(self):
        with patch(
            "sys.argv",
            [
                "generate_report.py",
                "--input",
                "custom/input.csv",
                "--output",
                "custom/report.md",
            ],
        ):
            args = generate_report.parse_args()

        self.assertEqual(args.input, Path("custom/input.csv"))
        self.assertEqual(args.output, Path("custom/report.md"))


if __name__ == "__main__":
    unittest.main()
