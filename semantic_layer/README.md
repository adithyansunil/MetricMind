# MetricMind Semantic Layer

The MetricMind Semantic Layer provides governed definitions
for business metrics and analytical dimensions.

## Purpose

The Semantic Layer prevents the AI agent from directly
querying raw database tables and inventing business logic.

Instead, the agent works with predefined metrics and dimensions.

## Measures

- Revenue
- Cost
- Profit
- Margin
- Units Sold

## Dimensions

### Time
- Date
- Month
- Quarter
- Year

### Geography
- Region
- Country

### Product
- Product

## Metric Definitions

Revenue:
SUM(sales.revenue)

Cost:
SUM(sales.cost)

Profit:
Revenue - Cost

Margin:
Profit / Revenue * 100

Units Sold:
SUM(sales.units)

## Architecture

User Question
      ↓
LLM Agent
      ↓
Semantic Layer
      ↓
Governed Metric Definition
      ↓
PostgreSQL
      ↓
Structured JSON Result