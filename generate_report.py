import argparse
from pathlib import Path

from parallel.config import DATA_PATH, REPORT_PATH
from parallel import generate_report


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a vending decision report.")
    parser.add_argument(
        "--input",
        default=DATA_PATH,
        type=Path,
        help=f"CSV input path. Defaults to {DATA_PATH}.",
    )
    parser.add_argument(
        "--output",
        default=REPORT_PATH,
        type=Path,
        help=f"Markdown output path. Defaults to {REPORT_PATH}.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_report(data_path=args.input, report_path=args.output)
