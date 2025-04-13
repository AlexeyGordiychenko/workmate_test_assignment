import argparse
from collections import defaultdict
from pathlib import Path


def check_log_files_exist(log_files):
    return [log_file for log_file in log_files if not Path(log_file).exists()]


def process_log_file(log_file):
    with open(log_file, "r") as f:
        counts = defaultdict(lambda: defaultdict(int))
        for line in f:
            if "django.request" in line:
                parts = line.split(" ")
                level = parts[2]
                endpoint = next((x for x in parts if x.startswith("/")), None)
                counts[endpoint][level] += 1
    print(f"\nLog file: {log_file}")
    for endpoint in sorted(counts.keys()):
        print(endpoint)
        for level in counts[endpoint]:
            print(f"  {level}: {counts[endpoint][level]}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse Django log files and count log levels per endpoint."
    )
    parser.add_argument("log_files", nargs="+", type=str, help="Log files to parse.")
    parser.add_argument(
        "--report",
        "-r",
        type=str,
        choices=["handlers"],
        help="Type of report.",
        required=True,
    )
    args = parser.parse_args()
    return args.report, set(args.log_files)


def main():
    report, log_files = parse_args()
    error_log_files = check_log_files_exist(log_files)
    if error_log_files:
        print(
            "Error: The following log files do not exist:",
            "\n".join(error_log_files),
            sep="\n",
        )
        return
    for log_file in log_files:
        process_log_file(log_file)


if __name__ == "__main__":
    main()
