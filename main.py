import argparse
import os
from collections import defaultdict
from multiprocessing import Pool
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
                if endpoint:
                    counts[endpoint.strip()][level] += 1
    return dict(counts)


def merge_log_files_data(results):
    merged_counts = defaultdict(lambda: defaultdict(int))
    total_count = 0
    max_endpoint_len = 0

    for result in results:
        for endpoint, levels in result.items():
            for level, count in levels.items():
                merged_counts[endpoint][level] += count
                total_count += count
                max_endpoint_len = max(max_endpoint_len, len(endpoint))
    return merged_counts, total_count, max_endpoint_len


def output_report(counts, total_count, endpoint_max_len):
    levels = {level: 0 for level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")}
    column_width = max(len(level) for level in levels) + 1
    endpoint_max_len += 1
    print(f"Total requests: {total_count}\n")
    print(f"{'HANDLER':<{endpoint_max_len}}", end="")
    for level in levels:
        print(f"{level:<{column_width}}", end="")
    print()
    for endpoint in sorted(counts.keys()):
        print(f"{endpoint:<{endpoint_max_len}}", end="")
        for level in levels:
            print(f"{counts[endpoint][level]:<{column_width}}", end="")
            levels[level] += counts[endpoint][level]
        print()
    print(" " * endpoint_max_len, end="")
    for level in levels.values():
        print(f"{level:<{column_width}}", end="")
    print()


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
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_log_file, log_files)
    merge_counts, total_count, max_endpoint_len = merge_log_files_data(results)
    output_report(merge_counts, total_count, max_endpoint_len)


if __name__ == "__main__":
    main()
