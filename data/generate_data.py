import csv
import random
from datetime import date, timedelta
from pathlib import Path

# ============================================
# MetricMind - Synthetic Corporate Data
# ============================================

random.seed(42)

OUTPUT_FILE = Path(__file__).parent / "corporate_sales.csv"

# Regional structure
REGIONS = {
    "Europe": [
        "Germany",
        "France",
        "United Kingdom",
        "Italy",
        "Spain",
        "Netherlands",
    ],
    "Asia": [
        "India",
        "Japan",
        "Singapore",
        "South Korea",
        "Malaysia",
    ],
    "North America": [
        "United States",
        "Canada",
        "Mexico",
    ],
    "South America": [
        "Brazil",
        "Argentina",
        "Chile",
    ],
}

# Product configuration
PRODUCTS = {
    "Laptop": {
        "price_range": (800, 1800),
        "cost_ratio": (0.62, 0.78),
    },
    "Smartphone": {
        "price_range": (400, 1200),
        "cost_ratio": (0.58, 0.74),
    },
    "Tablet": {
        "price_range": (300, 900),
        "cost_ratio": (0.55, 0.72),
    },
    "Monitor": {
        "price_range": (200, 700),
        "cost_ratio": (0.60, 0.76),
    },
    "Headphones": {
        "price_range": (80, 350),
        "cost_ratio": (0.45, 0.68),
    },
}

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 6, 30)

NUMBER_OF_RECORDS = 15000


def random_date(start, end):
    """Generate a random date between two dates."""
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def generate_transaction(sale_id):
    """Generate one realistic sales transaction."""

    sale_date = random_date(START_DATE, END_DATE)

    region = random.choice(list(REGIONS.keys()))
    country = random.choice(REGIONS[region])
    product = random.choice(list(PRODUCTS.keys()))

    product_info = PRODUCTS[product]

    # Random quantity
    units = random.randint(1, 30)

    # Product selling price
    price = random.uniform(
        product_info["price_range"][0],
        product_info["price_range"][1],
    )

    revenue = price * units

    # Base cost ratio
    cost_ratio = random.uniform(
        product_info["cost_ratio"][0],
        product_info["cost_ratio"][1],
    )

    # Create a controlled European margin reduction
    # during Q2 2026 for future root-cause analysis.
    if region == "Europe" and sale_date >= date(2026, 4, 1):
        cost_ratio += 0.08

    # Small regional variation
    if region == "Asia":
        cost_ratio += 0.01
    elif region == "North America":
        cost_ratio -= 0.01

    cost = revenue * min(cost_ratio, 0.95)

    return {
        "sale_id": sale_id,
        "sale_date": sale_date.isoformat(),
        "region": region,
        "country": country,
        "product": product,
        "units": units,
        "revenue": round(revenue, 2),
        "cost": round(cost, 2),
    }


def main():
    print("Generating MetricMind corporate sales data...")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "sale_id",
            "sale_date",
            "region",
            "country",
            "product",
            "units",
            "revenue",
            "cost",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for sale_id in range(1, NUMBER_OF_RECORDS + 1):
            writer.writerow(generate_transaction(sale_id))

    print(f"Generated {NUMBER_OF_RECORDS:,} transactions.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()