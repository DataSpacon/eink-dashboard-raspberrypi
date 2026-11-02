import json
import sqlite3
import sys
from datetime import date, datetime

from news import get_news
from weather import get_weather

DATABASE = "dashboard.db"


def get_daily_data(month, day):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT imieniny
        FROM days
        WHERE month = ? AND day = ?
    """, (month, day))

    row = cursor.fetchone()
    imieniny = row[0] if row else ""

    cursor.execute("""
        SELECT text
        FROM advice
        WHERE month = ? AND day = ?
    """, (month, day))

    row = cursor.fetchone()
    advice = row[0] if row else ""

    connection.close()

    return imieniny, advice


def get_dashboard_data(selected_date):
    imieniny, advice = get_daily_data(
        selected_date.month,
        selected_date.day
    )

    return {
        "date": selected_date.isoformat(),
        "weekday": selected_date.strftime("%A"),
        "month": selected_date.strftime("%B"),
        "imieniny": imieniny,
        "advice": advice,
        "weather": get_weather(),
        "news": get_news()
    }


def get_selected_date():
    if len(sys.argv) == 1:
        return date.today()

    if len(sys.argv) != 2:
        print("Usage: python dashboard.py [YYYY-MM-DD]")
        sys.exit(1)

    try:
        return datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        sys.exit(1)


if __name__ == "__main__":
    selected_date = get_selected_date()
    data = get_dashboard_data(selected_date)

    print(json.dumps(data, ensure_ascii=False, indent=2))
