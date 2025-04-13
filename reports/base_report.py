import os
import sys
from multiprocessing import Pool
from pathlib import Path


class BaseReport:
    def __init__(self, log_files):
        self.log_files = log_files

    @property
    def missing_log_files(self):
        return [log_file for log_file in self.log_files if not Path(log_file).exists()]

    def output_missing_log_files(self, missing_log_files):
        print(
            "Error: The following log files do not exist:",
            "\n".join(missing_log_files),
            sep="\n",
            file=sys.stderr,
        )

    def process_log_file(self, log_file):
        pass

    def process_log_files_in_parallel(self):
        with Pool(processes=os.cpu_count()) as pool:
            return pool.map(self.process_log_file, self.log_files)

    def generate_report(self):
        raise NotImplementedError
