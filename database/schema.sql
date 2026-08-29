-- ============================================
-- MetricMind Database Schema
-- ============================================

-- Drop table if it already exists
DROP TABLE IF EXISTS sales;

-- Main corporate sales fact table
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL,
    product VARCHAR(100) NOT NULL,
    units INTEGER NOT NULL CHECK (units > 0),
    revenue NUMERIC(15, 2) NOT NULL CHECK (revenue >= 0),
    cost NUMERIC(15, 2) NOT NULL CHECK (cost >= 0)
);

-- Indexes for common analytical filters
CREATE INDEX idx_sales_date
    ON sales(sale_date);

CREATE INDEX idx_sales_region
    ON sales(region);

CREATE INDEX idx_sales_country
    ON sales(country);

CREATE INDEX idx_sales_product
    ON sales(product);