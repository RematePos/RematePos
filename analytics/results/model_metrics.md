# Sales Prediction Model Metrics

## Model

- Model: `RandomForestRegressor`
- Dataset: `analytics/data/sample_sales_data.csv`
- Target: `sale_total`
- Records: `150`
- Train records: `120`
- Test records: `30`
- Random state: `42`

## Metrics

| Metric | Value |
| --- | ---: |
| MAE | 8375.7765 |
| RMSE | 12996.3302 |
| R2 | 0.8928 |

## Feature Columns

- `product_id`
- `quantity_sold`
- `unit_price`
- `stock_available`
- `return_flag`
- `day_of_week`
- `month`
- `is_weekend`
- `category_cleaning`
- `category_groceries`
- `category_household`
- `category_personal_care`
- `category_snacks`
- `payment_method_CARD`
- `payment_method_CASH`
- `payment_method_NEQUI`
- `payment_method_PSE`

## Scope

These metrics were generated from a synthetic non-sensitive academic proof-of-concept dataset. This model is not deployed to production and no model artifact was persisted.
