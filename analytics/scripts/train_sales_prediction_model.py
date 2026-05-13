"""Train a small sales prediction proof of concept for RematePOS.

This script uses synthetic non-sensitive sales data. It performs basic
validation, feature engineering, model training, and metric export.

It intentionally does not persist a production model artifact.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


ANALYTICS_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ANALYTICS_DIR / "data" / "sample_sales_data.csv"
RESULTS_DIR = ANALYTICS_DIR / "results"
METRICS_JSON_PATH = RESULTS_DIR / "model_metrics.json"
METRICS_MD_PATH = RESULTS_DIR / "model_metrics.md"

REQUIRED_COLUMNS = [
    "sale_date",
    "product_id",
    "category",
    "quantity_sold",
    "unit_price",
    "stock_available",
    "payment_method",
    "return_flag",
]

BASE_FEATURES = [
    "product_id",
    "quantity_sold",
    "unit_price",
    "stock_available",
    "return_flag",
    "day_of_week",
    "month",
    "is_weekend",
]

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    data = pd.read_csv(path)
    missing = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    return data


def transform_dataset(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    transformed = data.copy()
    transformed["sale_date"] = pd.to_datetime(transformed["sale_date"], errors="raise")
    transformed["day_of_week"] = transformed["sale_date"].dt.dayofweek
    transformed["month"] = transformed["sale_date"].dt.month
    transformed["is_weekend"] = transformed["day_of_week"].isin([5, 6]).astype(int)
    transformed["sale_total"] = transformed["quantity_sold"] * transformed["unit_price"]

    categorical = pd.get_dummies(
        transformed[["category", "payment_method"]],
        prefix=["category", "payment_method"],
        dtype=int,
    )

    features = pd.concat([transformed[BASE_FEATURES], categorical], axis=1)
    target = transformed["sale_total"]

    return features, target, list(features.columns)


def train_and_evaluate(features: pd.DataFrame, target: pd.Series) -> dict:
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=RANDOM_STATE,
        min_samples_leaf=2,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    r2 = r2_score(y_test, predictions)

    return {
        "model": "RandomForestRegressor",
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "records": int(len(target)),
        "train_records": int(len(y_train)),
        "test_records": int(len(y_test)),
        "metrics": {
            "mae": round(float(mae), 4),
            "rmse": round(float(rmse), 4),
            "r2": round(float(r2), 4),
        },
    }


def write_metrics(metrics: dict, feature_columns: list[str]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        **metrics,
        "target": "sale_total",
        "feature_columns": feature_columns,
        "dataset": "analytics/data/sample_sales_data.csv",
        "data_note": "Synthetic non-sensitive academic proof-of-concept dataset.",
        "production_status": "Not a production model.",
    }

    METRICS_JSON_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    metric_values = payload["metrics"]
    markdown = f"""# Sales Prediction Model Metrics

## Model

- Model: `{payload["model"]}`
- Dataset: `{payload["dataset"]}`
- Target: `{payload["target"]}`
- Records: `{payload["records"]}`
- Train records: `{payload["train_records"]}`
- Test records: `{payload["test_records"]}`
- Random state: `{payload["random_state"]}`

## Metrics

| Metric | Value |
| --- | ---: |
| MAE | {metric_values["mae"]} |
| RMSE | {metric_values["rmse"]} |
| R2 | {metric_values["r2"]} |

## Feature Columns

{chr(10).join(f"- `{column}`" for column in feature_columns)}

## Scope

These metrics were generated from a synthetic non-sensitive academic proof-of-concept dataset. This model is not deployed to production and no model artifact was persisted.
"""

    METRICS_MD_PATH.write_text(markdown, encoding="utf-8")


def main() -> None:
    data = load_dataset(DATA_PATH)
    features, target, feature_columns = transform_dataset(data)
    metrics = train_and_evaluate(features, target)
    write_metrics(metrics, feature_columns)

    print("RematePOS predictive model POC")
    print(f"Records: {metrics['records']}")
    print(f"Feature columns: {', '.join(feature_columns)}")
    print(f"Model: {metrics['model']}")
    print(f"MAE: {metrics['metrics']['mae']}")
    print(f"RMSE: {metrics['metrics']['rmse']}")
    print(f"R2: {metrics['metrics']['r2']}")
    print(f"Metrics JSON: {METRICS_JSON_PATH}")
    print(f"Metrics Markdown: {METRICS_MD_PATH}")


if __name__ == "__main__":
    main()
