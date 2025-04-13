import os
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import List, Set


class BaseReport:
    def __init__(self, log_files: Set[str]) -> None:
        self.log_files = log_files

    @property
    def missing_log_files(self) -> List[str]:
        return [log_file for log_file in self.log_files if not Path(log_file).exists()]

    def output_missing_log_files(
        self, missing_log_files: List[str]
    ) -> None:  # pragma: no cover
        print(
            "Error: The following log files do not exist:",
            "\n".join(missing_log_files),
            sep="\n",
            file=sys.stderr,
        )

    def process_log_file(self, log_file: str) -> None:  # pragma: no cover
        pass

    def process_log_files_in_parallel(self) -> List:  # pragma: no cover
        with Pool(processes=os.cpu_count()) as pool:
            return pool.map(self.process_log_file, self.log_files)

    def generate_report(self) -> None:  # pragma: no cover
        raise NotImplementedError
