import sqlite3

DATABASE = "dashboard.db"


def add_test_data():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO days (month, day, imieniny)
        VALUES (?, ?, ?)
    """, (9, 2, "Stefan, Julian"))

    cursor.execute("""
        INSERT OR REPLACE INTO days (month, day, imieniny)
        VALUES (?, ?, ?)
    """, (9, 3, "Izabela, Szymon"))

    cursor.execute("""
        INSERT OR REPLACE INTO advice (month, day, text)
        VALUES (?, ?, ?)
    """, (9, 2, "Get off!"))

    cursor.execute("""
        INSERT OR REPLACE INTO advice (month, day, text)
        VALUES (?, ?, ?)
    """, (9, 3, "Take a break and enjoy the day."))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    add_test_data()
    print("Test data added successfully.")
