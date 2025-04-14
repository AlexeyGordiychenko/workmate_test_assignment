import argparse
from typing import List

from reports import report_types


def parse_args(args: List[str] = None) -> tuple:
    parser = argparse.ArgumentParser(description="Log analyzer for Django apps.")
    parser.add_argument("log_files", nargs="+", type=str, help="Log files to parse.")
    parser.add_argument(
        "--report",
        "-r",
        type=str,
        choices=[key for key in report_types.keys()],
        help="Type of report.",
        required=True,
    )
    args = parser.parse_args(args)
    return args.report, set(args.log_files)


def main() -> None:  # pragma: no cover
    report, log_files = parse_args()
    report = report_types[report](log_files)
    report.generate_report()


if __name__ == "__main__":
    main()  # pragma: no cover
