from collections import Counter, defaultdict

from reports.base_report import BaseReport


class HandlersReport(BaseReport):
    def __init__(self, log_files):
        super().__init__(log_files)
        self.levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.data = {}
        self.total_count = 0
        self.endpoint_max_len = 10
        self.column_width = max(len(level) for level in self.levels)

    def generate_report(self):  # pragma: no cover
        missing_log_files = self.missing_log_files
        if missing_log_files:
            self.output_missing_log_files(missing_log_files)
            return

        self.merge_log_files_data(self.process_log_files_in_parallel())
        self.output_report()

    def process_log_file(self, log_file):
        with open(log_file, "r") as f:
            counts = defaultdict(Counter)
            for line in f:
                if "django.request" in line:
                    parts = line.split(" ")
                    level = parts[2] if len(parts) > 2 else ""
                    endpoint = next((x for x in parts if x.startswith("/")), None)
                    if endpoint:
                        counts[endpoint.strip()][level] += 1
        return counts

    def merge_log_files_data(self, results):
        merged_counts = defaultdict(Counter)

        for result in results:
            for endpoint, levels in result.items():
                for level, count in levels.items():
                    merged_counts[endpoint][level] += count
                    self.total_count += count
                    self.endpoint_max_len = max(self.endpoint_max_len, len(endpoint))
        self.data = merged_counts

    def output_report(self):  # pragma: no cover
        levels_count = defaultdict(int)
        self.endpoint_max_len += 1
        self.column_width += 1

        print(f"Total requests: {self.total_count}\n")
        print(f"{'HANDLER':<{self.endpoint_max_len}}", end="")
        for level in self.levels:
            print(f"{level:<{self.column_width}}", end="")
        print()
        for endpoint in sorted(self.data.keys()):
            print(f"{endpoint:<{self.endpoint_max_len}}", end="")
            for level in self.levels:
                print(f"{self.data[endpoint][level]:<{self.column_width}}", end="")
                levels_count[level] += self.data[endpoint][level]
            print()
        print(" " * self.endpoint_max_len, end="")
        for level in levels_count.values():
            print(f"{level:<{self.column_width}}", end="")
        print()
