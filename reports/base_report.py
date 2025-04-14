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
        """
        List of non-existent log files.

        :return: List of paths to non-existent log files.
        """
        return [log_file for log_file in self.log_files if not Path(log_file).exists()]

    def output_missing_log_files(
        self, missing_log_files: List[str]
    ) -> None:  # pragma: no cover
        """
        Outputs a list of missing log files to standard error.

        :param missing_log_files: List of paths to non-existent log files.
        """
        print(
            "Error: The following log files do not exist:",
            "\n".join(missing_log_files),
            sep="\n",
            file=sys.stderr,
        )

    def process_log_file(self, log_file: str) -> None:  # pragma: no cover
        # not NotImplementedError because the function is not mandatory
        pass

    def process_log_files_in_parallel(self) -> List:  # pragma: no cover
        """
        Process multiple log files in parallel and return the results.

        :return: List of results from processing each log file.
        """
        with Pool(processes=os.cpu_count()) as pool:
            return pool.map(self.process_log_file, self.log_files)

    def generate_report(self) -> None:  # pragma: no cover
        # mandatory function, every report must implement
        raise NotImplementedError
