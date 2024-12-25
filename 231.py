import sqlite3
import os

db_path = 'Z:/OpenGameMusic/OpenGameMusic.db'

if not os.path.exists(db_path):
    print("Файл базы данных не найден.")
else:
    try:
        connection = sqlite3.connect(db_path)
        print("Подключение успешно!")
        connection.close()
    except sqlite3.Error as e:
        print("Ошибка подключения:", e)
