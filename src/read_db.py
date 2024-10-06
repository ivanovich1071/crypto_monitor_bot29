import sqlite3

# Путь к файлу базы данных
db_path = "users.db"

def read_db():
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Пример запроса для получения всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Выводим список таблиц
    print("Список таблиц в базе данных:")
    for table in tables:
        print(table[0])

    # Пример запроса для чтения данных из таблицы 'users' (или другой существующей таблицы)
    # Замените 'users' на название вашей таблицы
    table_name = 'users'  # замените на нужное имя таблицы
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Выводим строки таблицы
        print(f"\nДанные из таблицы '{table_name}':")
        for row in rows:
            print(row)
    except sqlite3.OperationalError as e:
        print(f"Ошибка при чтении таблицы '{table_name}':", e)

    # Закрываем соединение с базой данных
    conn.close()

if __name__ == "__main__":
    read_db()
