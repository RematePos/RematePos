# Predictive Model Process

## Purpose

This document defines a responsible predictive model process for future RematePOS work.

It does not claim that a production predictive model already exists. The HU-125 audit did not find a trained model, dataset, metrics, or prediction endpoint in the reviewed repositories.

## Candidate Prediction Problems

Future predictive work may focus on:

- daily sales prediction;
- product demand prediction;
- low stock alerting;
- ranking of top-selling products;
- return frequency analysis;
- payment method distribution analysis.

## Recommended Proof Of Concept

The recommended HU-126 proof of concept is:

Predict daily sales or product demand using synthetic or anonymized non-sensitive data.

Suggested target options:

- `daily_sales_total`;
- `quantity_sold`.

Suggested baseline algorithms:

- `LinearRegression`;
- `RandomForestRegressor`.

Suggested metrics for numeric prediction:

- MAE;
- RMSE;
- R2.

These metrics should only be reported after a real POC is implemented and executed. No metrics are reported in HU-125 because no model was found during the audit.

## Minimum POC Workflow

1. Define the prediction objective.
2. Define the dataset schema.
3. Generate or prepare synthetic/anonymized data.
4. Validate that no personal data exists in the dataset.
5. Transform dates, categories, quantities, prices, and payment information.
6. Create features.
7. Split train/test data.
8. Train a baseline model.
9. Evaluate with MAE, RMSE, and R2.
10. Document limitations.
11. Keep the model out of production until reviewed.

## Candidate Dataset Columns

| Column | Description |
| --- | --- |
| `sale_date` | Sale date |
| `day_of_week` | Derived weekday |
| `month` | Derived month |
| `product_id` | Product identifier |
| `category` | Product category |
| `quantity_sold` | Units sold |
| `unit_price` | Product unit price |
| `sale_total` | Total sale value |
| `payment_method` | Cash, card, PSE, Nequi, etc. |
| `stock_available` | Stock available at sale time |
| `return_flag` | Whether the item was returned |

## Model Governance

Any future predictive model must document:

- dataset origin;
- anonymization or synthetic data strategy;
- transformation steps;
- feature list;
- target variable;
- algorithm;
- training command;
- evaluation metrics;
- known limitations;
- whether the model is offline, experimental, or integrated.

## Integration Boundaries

The model should not be exposed through backend or frontend until:

- the POC is reviewed;
- metrics are available;
- limitations are documented;
- data privacy has been checked;
- the team approves the integration scope.

## Current Status

As of HU-125:

- no production predictive model exists;
- no trained model artifact exists;
- no metrics exist;
- no dataset is versioned;
- no prediction endpoint exists;
- HU-126 should implement a controlled POC if the team needs predictive evidence.

## Security Rules

Do not commit:

- real customer data;
- personal identifiers;
- database dumps;
- backup files;
- secrets;
- `.env` files;
- large model artifacts;
- generated datasets without review.

## Limitations

The first model should be treated as educational and exploratory. It should not be used for commercial decisions until validated with enough historical data and reviewed for bias, leakage, quality, and business usefulness.
