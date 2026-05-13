# Data Transformation Process

## Purpose

This document defines the proposed data transformation process for future analytics and predictive modeling in RematePOS.

It is a design and planning document. It does not claim that a production transformation pipeline already exists.

## Potential Data Sources

Future data transformation work may use non-sensitive data from:

- sales or purchases;
- invoices;
- products;
- inventory;
- customers after anonymization;
- payments;
- returns.

## Candidate Variables

Possible variables for a future dataset include:

| Variable | Description | Sensitivity |
| --- | --- | --- |
| `sale_date` | Date of sale or purchase | Low |
| `sale_hour` | Hour of sale | Low |
| `day_of_week` | Derived weekday | Low |
| `month` | Derived month | Low |
| `product_id` | Product identifier | Medium |
| `product_category` | Product category | Low |
| `quantity_sold` | Units sold | Low |
| `unit_price` | Product unit price | Low |
| `sale_total` | Total sale amount | Low |
| `payment_method` | Cash, card, PSE, Nequi, etc. | Low |
| `payment_status` | Approved, pending, failed, etc. | Low |
| `stock_available` | Stock at or near sale time | Low |
| `return_flag` | Whether the sale had a return | Low |
| `returned_quantity` | Units returned | Low |

Customer names, identification numbers, phone numbers, emails, and addresses should not be used directly in a predictive dataset.

## Transformation Steps

Recommended transformation flow:

1. Extract only the required fields from operational tables or service responses.
2. Remove or anonymize personal data.
3. Validate required columns.
4. Validate null values.
5. Convert dates and timestamps to consistent formats.
6. Create date-derived features such as day of week, month, hour, and week number.
7. Normalize categorical values such as payment method and payment status.
8. Aggregate sales by day, product, or category depending on the model objective.
9. Handle returns by subtracting returned quantities or adding return-specific features.
10. Validate numeric ranges such as quantity, price, stock, subtotal, tax, and total.
11. Split data into train and test sets.
12. Save only non-sensitive intermediate artifacts if they are needed for review.

## Example Feature Sets

### Daily Sales Prediction

Possible target:

- `daily_sales_total`

Possible features:

- day of week;
- month;
- number of transactions;
- average ticket value;
- total items sold;
- number of returns;
- payment method distribution.

### Product Demand Prediction

Possible target:

- `quantity_sold`

Possible features:

- product category;
- product price;
- stock available;
- day of week;
- month;
- recent sales rolling average;
- return frequency.

### Low Stock Alert

Possible target:

- whether a product may fall below a stock threshold.

Possible features:

- current stock;
- recent sales velocity;
- average quantity sold per day;
- lead time estimate;
- category.

## Data Validation Rules

Before training any model, the dataset should be validated for:

- missing required columns;
- duplicated records;
- invalid dates;
- negative prices;
- negative quantities;
- inconsistent payment statuses;
- inconsistent invoice or purchase identifiers;
- records with personal data that should be excluded;
- train/test leakage.

## Train/Test Split

For time-based sales data, avoid random split as the default approach.

Recommended split:

- train on earlier dates;
- test on later dates.

This better simulates the real forecasting scenario.

## Security Rules

Do not commit:

- real customer personal data;
- raw production exports;
- database dumps;
- backups;
- full logs;
- `.env` files;
- credentials;
- large generated datasets;
- model artifacts without review.

## Current Status

As of HU-125, this process is proposed and documented. The audit did not find an existing implemented transformation pipeline or trained predictive model.
