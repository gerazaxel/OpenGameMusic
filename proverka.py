import sqlite3

try:
    connection = sqlite3.connect(
        host='localhost',
        user='username',
        password='password',
        database='OpenGameMusic'
    )
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
