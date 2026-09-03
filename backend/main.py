from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

from backend.semantic_engine import (
    get_metric,
    get_available_metrics,
    get_available_dimensions,
)

# ============================================
# MetricMind - FastAPI Backend
# ============================================

load_dotenv()

app = FastAPI(
    title="MetricMind API",
    description="Governed Semantic BI API",
    version="1.0.0",
)

# Allow the Next.js frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    """Create a PostgreSQL database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "metricmind"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )


@app.get("/")
def root():
    return {
        "application": "MetricMind",
        "description": "Agentic Semantic BI Engine",
        "status": "running",
    }


@app.get("/api/semantic/metrics")
def available_metrics():
    """Return all governed metrics."""
    return {
        "metrics": get_available_metrics()
    }


@app.get("/api/semantic/dimensions")
def available_dimensions():
    """Return all available dimensions."""
    return {
        "dimensions": get_available_dimensions()
    }


@app.get("/api/metrics/{metric_name}")
def get_metric_value(
    metric_name: str,
    region: str | None = Query(default=None),
    country: str | None = Query(default=None),
    product: str | None = Query(default=None),
):
    """
    Calculate a governed metric using the Semantic Layer.
    """

    try:
        metric = get_metric(metric_name)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown metric: {metric_name}"
        )

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        filters = []
        parameters = []

        if region:
            filters.append("region = %s")
            parameters.append(region)

        if country:
            filters.append("country = %s")
            parameters.append(country)

        if product:
            filters.append("product = %s")
            parameters.append(product)

        where_clause = ""

        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        metric_type = metric["type"]

        if metric_type == "sum":
            column = metric["source_column"]

            query = f"""
                SELECT COALESCE(SUM({column}), 0)
                FROM sales
                {where_clause}
            """

            cursor.execute(query, parameters)
            value = cursor.fetchone()[0]

        elif metric_name.lower() == "profit":

            query = f"""
                SELECT COALESCE(SUM(revenue - cost), 0)
                FROM sales
                {where_clause}
            """

            cursor.execute(query, parameters)
            value = cursor.fetchone()[0]

        elif metric_name.lower() == "margin":

            query = f"""
                SELECT
                    CASE
                        WHEN SUM(revenue) = 0 THEN 0
                        ELSE
                            (SUM(revenue - cost) / SUM(revenue)) * 100
                    END
                FROM sales
                {where_clause}
            """

            cursor.execute(query, parameters)
            value = cursor.fetchone()[0]

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Metric calculation not implemented: {metric_name}"
            )

        return {
            "metric": metric["name"],
            "filters": {
                "region": region,
                "country": country,
                "product": product,
            },
            "value": float(value),
        }

    finally:
        cursor.close()
        connection.close()