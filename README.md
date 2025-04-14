Русский | [English](README_ENG.md)

## Анализ журнала логирования django-приложения

Это CLI-приложение для анализа логов django-приложения.

### Технологии
- 🐍 Стандартная библиотека Python
- ✅ Тесты с помощью Pytest.

### Функциональность

- Анализ логов и формирование отчетов
- Обработка больших файлов в несколько гигабайт
- Обработка нескольких файлов логов параллельно

### Использование

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

### Доступные отчеты

#### 1. Handlers

Формирование отчета `handlers` в разрезе эндпоинтов и уровней логирования.


Пример формирование отчёта:
```
python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
```

Пример вывода отчета:

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

## Структура проекта

```
.
├── main.py                 # точка входа
├── reports                 # классы доступных отчетов
│   ├── base_report.py      # базовый класс отчета
│   ├── handlers_report.py  # класс отчета handlers
│   ├── __init__.py         # инициализация пакета reports
├── requirements.txt        # зависимости
├── tests/                  # тесты
```

## Установка

Клонирование репозитория:

```
git clone https://github.com/AlexeyGordiychenko/workmate_test_assignment.git
cd workmate_test_assignment
```

Создание и активация виртуального окружения


```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Особенности

В архитектуру приложения заложена возможность удобного добавления новых видов отчётов. Для добавления нового вида необходимо создать новый модуль в папке `reports` с новым классом отчета, наследующим `BaseReport`, и добавить его в словарь `report_types`.

## Тестирование

Для запуска тестов необходимо выполнить команду:

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