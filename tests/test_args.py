import pytest

from main import parse_args


def test_parse_args_valid_input_short() -> None:
    report, log_files = parse_args(["-r", "handlers", "file1.log", "file2.log"])
    assert report == "handlers"
    assert log_files == {"file1.log", "file2.log"}


def test_parse_args_valid_input_long() -> None:
    report, log_files = parse_args(["--report", "handlers", "file1.log", "file2.log"])
    assert report == "handlers"
    assert log_files == {"file1.log", "file2.log"}


def test_parse_args_valid_input_duplicates() -> None:
    report, log_files = parse_args(["--report", "handlers", "file1.log", "file1.log"])
    assert report == "handlers"
    assert log_files == {"file1.log"}


def test_parse_args_invalid_no_args() -> None:
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_invalid_no_files() -> None:
    with pytest.raises(SystemExit):
        parse_args(["-r", "test"])


def test_parse_args_invalid_no_report_type() -> None:
    with pytest.raises(SystemExit):
        parse_args(["file1.log", "file2.log"])


def test_parse_args_invalid_report_type() -> None:
    with pytest.raises(SystemExit):
        parse_args(["-r", "test", "file1.log", "file2.log"])


def test_parse_args_invalid_extra_args() -> None:
    with pytest.raises(SystemExit):
        parse_args(["-r", "handlers", "-t", "test", "file1.log", "file2.log"])
