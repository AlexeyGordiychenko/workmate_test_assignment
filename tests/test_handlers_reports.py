import pytest

from reports.handlers_report import HandlersReport


@pytest.fixture
def file1_data() -> tuple[int, dict]:
    return 63, {
        "/api/v1/reviews/": {"INFO": 5},
        "/admin/dashboard/": {"INFO": 6, "ERROR": 2},
        "/api/v1/users/": {"INFO": 4},
        "/api/v1/cart/": {"INFO": 3},
        "/api/v1/products/": {"INFO": 3},
        "/api/v1/support/": {"INFO": 1, "ERROR": 3, "CRITICAL": 1},
        "/api/v1/auth/login/": {"INFO": 4, "DEBUG": 1, "ERROR": 1},
        "/admin/login/": {"INFO": 5, "ERROR": 1},
        "/api/v1/checkout/": {"ERROR": 1, "INFO": 6},
        "/api/v1/payments/": {"INFO": 7, "WARNING": 1, "ERROR": 1},
        "/api/v1/orders/": {"INFO": 2, "ERROR": 2},
        "/api/v1/shipping/": {"INFO": 2, "ERROR": 1},
    }


@pytest.fixture
def file2_data() -> tuple[int, dict]:
    return 62, {
        "/api/v1/checkout/": {"INFO": 5, "ERROR": 1},
        "/api/v1/users/": {"ERROR": 2, "INFO": 3},
        "/api/v1/orders/": {"INFO": 4, "ERROR": 1},
        "/api/v1/payments/": {"INFO": 3, "ERROR": 1},
        "/api/v1/auth/login/": {"INFO": 3},
        "/api/v1/products/": {"INFO": 5, "ERROR": 3},
        "/api/v1/reviews/": {"INFO": 8, "ERROR": 1},
        "/api/v1/support/": {"INFO": 8},
        "/admin/dashboard/": {"INFO": 4, "ERROR": 1},
        "/api/v1/shipping/": {"INFO": 3, "ERROR": 1},
        "/admin/login/": {"ERROR": 1, "INFO": 3},
        "/api/v1/cart/": {"INFO": 1},
    }


@pytest.fixture
def file1_file2_data() -> tuple[int, dict]:
    return 125, {
        "/api/v1/checkout/": {"INFO": 11, "ERROR": 2},
        "/api/v1/users/": {"ERROR": 2, "INFO": 7},
        "/api/v1/orders/": {"INFO": 6, "ERROR": 3},
        "/api/v1/payments/": {"INFO": 10, "ERROR": 2, "WARNING": 1},
        "/api/v1/auth/login/": {"INFO": 7, "DEBUG": 1, "ERROR": 1},
        "/api/v1/products/": {"INFO": 8, "ERROR": 3},
        "/api/v1/reviews/": {"INFO": 13, "ERROR": 1},
        "/api/v1/support/": {"INFO": 9, "ERROR": 3, "CRITICAL": 1},
        "/admin/dashboard/": {"INFO": 10, "ERROR": 3},
        "/api/v1/shipping/": {"INFO": 5, "ERROR": 2},
        "/admin/login/": {"ERROR": 2, "INFO": 8},
        "/api/v1/cart/": {"INFO": 4},
    }


def generate_report_no_multiprocessing(handlers_report: HandlersReport) -> None:
    handlers_report.merge_log_files_data(
        [handlers_report.process_log_file(file) for file in handlers_report.log_files]
    )


def test_handlers_report_file1(file1_data: tuple[int, dict]) -> None:
    handlers_report = HandlersReport({"./tests/logs/file1.log"})
    generate_report_no_multiprocessing(handlers_report)
    assert handlers_report.total_count == file1_data[0]
    assert handlers_report.data == file1_data[1]


def test_handlers_report_file2(file2_data: tuple[int, dict]) -> None:
    handlers_report = HandlersReport({"./tests/logs/file2.log"})
    generate_report_no_multiprocessing(handlers_report)
    assert handlers_report.total_count == file2_data[0]
    assert handlers_report.data == file2_data[1]


def test_handlers_report_file1_file2(file1_file2_data: tuple[int, dict]) -> None:
    handlers_report = HandlersReport(
        {"./tests/logs/file1.log", "./tests/logs/file2.log"}
    )
    generate_report_no_multiprocessing(handlers_report)
    assert handlers_report.total_count == file1_file2_data[0]
    assert handlers_report.data == file1_file2_data[1]


def test_handlers_report_empty_file() -> None:
    handlers_report = HandlersReport({"./tests/logs/file3.log"})
    generate_report_no_multiprocessing(handlers_report)
    assert handlers_report.total_count == 0
    assert handlers_report.data == {}


def test_handlers_report_no_endpoints() -> None:
    handlers_report = HandlersReport({"./tests/logs/file4.log"})
    generate_report_no_multiprocessing(handlers_report)
    assert handlers_report.total_count == 0
    assert handlers_report.data == {}


def test_handlers_report_incorrect_format() -> None:
    handlers_report = HandlersReport({"./tests/logs/file5.log"})
    generate_report_no_multiprocessing(handlers_report)
    assert handlers_report.total_count == 1
    assert handlers_report.data == {"/api/v1/reviews/": {"INFO": 1}}


def test_handlers_report_missing_log() -> None:
    handlers_report = HandlersReport({"./tests/logs/missing.log"})
    handlers_report.generate_report()
    assert handlers_report.missing_log_files == ["./tests/logs/missing.log"]
    assert handlers_report.total_count == 0
    assert handlers_report.data == {}
