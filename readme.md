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
```

Настройка подключений правится внутри `guard.py` в блоке `DB_CONFIG`. Запуск контроля:
```bash
python guard.py
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
```

Configure target connection parameters in `guard.py` inside the `DB_CONFIG` section. Run the audit:
```bash
python guard.py
```
