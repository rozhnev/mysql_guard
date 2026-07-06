# Описание
Утилита автоматического код-ревью структуры таблиц MySQL, заточенная под проверку проектов по стандартам ИТ-отделения РКСИ. Скрипт анализирует метаданные живой базы данных через `information_schema` и выявляет классические архитектурные косяки.

## Логика проверок:
1. Контроль копеек. Чекает столбцы со словами price, cost, balance. Если там стоит FLOAT или INT - скрипт ругается, требуя DECIMAL.
2. Контроль связей. Вытаскивает списком таблицы, в которых полностью забыли про FOREIGN KEY.
3. Детект мусорных таблиц. Ищет пустые таблицы без данных, которые забыли удалить после тестов.

## Развертывание:
```bash
git clone https://github.com
cd mysql_guard
pip install pymysql
cp config.ini.example config.ini
```

Настройка подключений хранится в `config.ini` (не попадает в git). Каждая секция файла — это отдельная БД:

```ini
[default]
host = localhost
user = root
password = 123456
database = rksi_test
charset = utf8mb4
```

Запуск контроля (используется секция `default` по умолчанию):
```bash
python guard.py
```

Выбор другой БД по имени секции:
```bash
python guard.py --db another_db
```

---

# English Description
Automated schema linter and architecture auditor designed for MySQL databases. It performs static analysis of database metadata via `information_schema` to enforce data consistency and prevent common design anti-patterns.

## Operational Checks:
1. Financial Data Integrity. Scans column names for keywords (price, cost, balance) and flags imprecise FLOAT/INT types, enforcing exact DECIMAL constraints.
2. Referential Integrity. Detects orphaned or isolated tables lacking any FOREIGN KEY configuration.
3. Schema Cleanup. Identifies abandoned empty tables with zero rows left after testing phases.

## Quick Start:
```bash
git clone https://github.com
cd mysql_guard
pip install pymysql
cp config.ini.example config.ini
```

Connection parameters live in `config.ini` (git-ignored). Each section is a separate database:

```ini
[default]
host = localhost
user = root
password = 123456
database = rksi_test
charset = utf8mb4
```

Run the audit (uses the `default` section by default):
```bash
python guard.py
```

Target a different database by section name:
```bash
python guard.py --db another_db
```
