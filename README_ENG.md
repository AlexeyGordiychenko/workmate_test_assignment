[Русский](README.md) | English

## Log Analyzer for Django apps

CLI tool for analyzing logs from Django apps.

### Technology Stack
- 🐍 Python standard library
- ✅ Tests with Pytest.

### Features

- Log parsing and report output
- Processing of large log files
- Processing of multiple log files in parallel

### Usage

```
usage: python main.py [-h] --report {handlers} [log_file1, log_file2, ...]

Log analyzer for Django apps.

positional arguments:
  log_files             Log files to parse.

options:
  -h, --help            show this help message and exit
  --report {handlers}, -r {handlers}
                        Type of report.
```

### Available reports

#### 1. Handlers

Generating a report `handlers` grouped by endpoints and logging levels.

Example usage:
```
python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
```

Example output:

```
Total requests: 63

HANDLER             DEBUG    INFO     WARNING  ERROR    CRITICAL 
/admin/dashboard/   0        6        0        2        0        
/admin/login/       0        5        0        1        0        
/api/v1/auth/login/ 1        4        0        1        0        
/api/v1/cart/       0        3        0        0        0        
/api/v1/checkout/   0        6        0        1        0        
/api/v1/orders/     0        2        0        2        0        
/api/v1/payments/   0        7        1        1        0        
/api/v1/products/   0        3        0        0        0        
/api/v1/reviews/    0        5        0        0        0        
/api/v1/shipping/   0        2        0        1        0        
/api/v1/support/    0        1        0        3        1        
/api/v1/users/      0        4        0        0        0        
                    1        48       1        12       1   
```

## Project Structure

```
.
├── main.py                 # entrypoint
├── reports                 # classes of available reports
│   ├── base_report.py      # base class of report
│   ├── handlers_report.py  # class of report handlers
│   ├── __init__.py         # initialization of the reports package
├── requirements.txt        # dependencies
├── tests/                  # tests
```

## Installation

Clone repository:

```
git clone https://github.com/AlexeyGordiychenko/workmate_test_assignment.git
cd workmate_test_assignment
```

Create and activate virtual enviroment

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Architecture

Architecture of the application makes it easy to add new reports. To add a new report, create a new module in the `reports` folder with a new report class that inherits from `BaseReport`, and add it to the `report_types` dictionary.

## Tests

To run tests use:

```
pytest
```

```
сoverage: 
Name                         Stmts   Miss  Cover
------------------------------------------------
main.py                         10      0   100%
reports/__init__.py              2      0   100%
reports/base_report.py          11      0   100%
reports/handlers_report.py      31      0   100%
------------------------------------------------
TOTAL                           54      0   100%
================================================
15 passed in 0.10s
================================================
```