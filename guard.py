import pymysql
import sys

# Тимлид меняет эти данные под свою тестовую базу.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "rksi_test",
    "charset": "utf8mb4"
}

def run_schema_audit():
    print("=" * 60)
    print(" STARTING DATABASE ARCHITECTURE AUDIT [MYSQL_GUARD]")
    print("=" * 60)
    
    try:
        # Подключаемся к СУБД через библиотеку
        connection = pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[CRITICAL ERROR] Подключение к MySQL не удалось: {e}")
        sys.exit(1)

    try:
        with connection.cursor() as cursor:
            
            # Ищем колонки с FLOAT, DOUBLE или INT
            money_query = """
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                  AND (column_name LIKE '%price%' OR column_name LIKE '%balance%' OR column_name LIKE '%money%' OR column_name LIKE '%cost%')
                  AND data_type IN ('float', 'double', 'int');
            """
            cursor.execute(money_query)
            money_errors = cursor.fetchall()
            
            print("\n[ЭТАП 1] Проверка точности финансовых типов данных...")
            if money_errors:
                for row in money_errors:
                    print(f"  [!] КРИТИЧЕСКИЙ БАГ: Таблица '{row[0]}', Колонка '{row[1]}' использует тип '{row[2]}' для денег! Срочно изменить на DECIMAL.")
            else:
                print("  [OK] Все поля имеют правильный тип данных.")


            # Ищем таблицы, у которых не настроены внешние ключи
            fk_query = """
                SELECT t.table_name 
                FROM information_schema.tables t
                WHERE t.table_schema = DATABASE() 
                  AND t.table_type = 'BASE TABLE'
                  AND t.table_name NOT IN (
                      SELECT table_name 
                      FROM information_schema.key_column_usage 
                      WHERE table_schema = DATABASE() 
                        AND referenced_table_name IS NOT NULL
                  );
            """
            cursor.execute(fk_query)
            fk_errors = cursor.fetchall()
            
            print("\n[ЭТАП 2] Проверка ссылочной целостности (Поиск таблиц без Foreign Keys)...")
            if fk_errors:
                for row in fk_errors:
                    print(f"  [!] ОШИБКА СВЯЗЕЙ: Таблица '{row[0]}' изолирована и не имеет внешних ключей! Риск появления мусора.")
            else:
                print("  [OK] Все таблицы логически связаны на уровне СУБД.")


            # Находим таблицы, в которых после тестов осталось 0 строк
            empty_tables_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                  AND table_type = 'BASE TABLE' 
                  AND table_rows = 0;
            """
            cursor.execute(empty_tables_query)
            empty_errors = cursor.fetchall()
            
            print("\n[ЭТАП 3] Поиск забытых пустых таблиц (Очистка схемы)...")
            if empty_errors:
                for row in empty_errors:
                    print(f"  [?] ВНИМАНИЕ: Таблица '{row[0]}' пуста. Возможно, это мусор после тестов, который забыли удалить.")
            else:
                print("  [OK] Заброшенных пустых таблиц в схеме не обнаружено.")

    except Exception as err:
        print(f"[ERROR] Ошибка во время выполнения SQL-запросов: {err}")
    finally:
        connection.close()
        print("\n" + "=" * 60)
        print(" АУДИТ ЗАВЕРШЕН. КОД-РЕВЬЮ ВЫПОЛНЕНО.")
        print("=" * 60)

if __name__ == "__main__":
    run_schema_audit()
