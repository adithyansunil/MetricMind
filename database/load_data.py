import csv
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# ============================================
# MetricMind - Load Corporate Sales Data
# ============================================

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "metricmind"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

CSV_FILE = Path(__file__).parent.parent / "data" / "corporate_sales.csv"


def load_sales_data():
    print("Connecting to PostgreSQL...")

    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    print("Connected successfully.")
    print(f"Loading data from: {CSV_FILE}")

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        rows = [
            (
                row["sale_date"],
                row["region"],
                row["country"],
                row["product"],
                int(row["units"]),
                float(row["revenue"]),
                float(row["cost"]),
            )
            for row in reader
        ]

    print(f"Records prepared: {len(rows):,}")

    insert_query = """
        INSERT INTO sales
        (sale_date, region, country, product, units, revenue, cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_query, rows)

    connection.commit()

    print(f"Successfully inserted {cursor.rowcount:,} records.")

    cursor.close()
    connection.close()

    print("Database connection closed.")


if __name__ == "__main__":
    load_sales_data()