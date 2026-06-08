# MVP Scope

Parallel's first MVP is a lightweight decision report engine for vending operations.

The goal is not to build a fully autonomous vending system in the first version. The goal is to validate whether vending machine data can be transformed into useful, explainable, and human-supervised operational recommendations.

## What v0.1 Does

The first MVP will:

1. Import vending data from CSV
2. Calculate stockout risk
3. Calculate waste or slow-mover risk
4. Assign a basic service priority level
5. Generate a Weekly Decision Report

## What v0.1 Does Not Do

The first MVP will not include:

- Live telemetry integration
- Direct vending machine control
- Dynamic pricing
- Automated operational execution
- Advanced route optimization
- Supplier marketplace features
- Customer-level personal data analysis

## Validation Goal

The MVP should help answer one key question:

> Can Parallel turn available vending data into recommendations that operators understand, trust, and can act on?

## Data Strategy

The first version can work with:

- Simulated vending data
- Historical vending data
- Weekly exported CSV files
- Manually prepared operator data

Live integration can be added after the recommendation logic is validated.
