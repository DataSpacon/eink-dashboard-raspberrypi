import sqlite3

DATABASE = "dashboard.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS days (
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            imieniny TEXT NOT NULL,
            PRIMARY KEY (month, day)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advice (
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY (month, day)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
