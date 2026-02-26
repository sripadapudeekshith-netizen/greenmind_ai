"""
GreenMind AI – Model Trainer
Trains a RandomForestRegressor on energy usage data and saves the model.

Usage:
    python models/train.py
"""

import os
import sys

# Ensure stdout can handle utf-8 characters properly on Windows
sys.stdout.reconfigure(encoding='utf-8')

# ── Ensure project root is on sys.path ─────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# ── Paths ───────────────────────────────────────────────────────────────────
DATA_PATH  = os.path.join(ROOT, "data", "energy_data.csv")
MODEL_DIR  = os.path.join(ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "energy_model.pkl")

FEATURES = ["temperature", "humidity", "hour"]
TARGET   = "energy_usage"


def load_data(path: str) -> pd.DataFrame:
    """Load and validate the dataset."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at '{path}'.\n"
            "Please ensure 'data/energy_data.csv' exists before training."
        )
    df = pd.read_csv(path)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    return df


def train(df: pd.DataFrame):
    """Train a RandomForestRegressor and return the fitted model."""
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return model, r2, X_test, y_pred


def save_model(model, path: str):
    """Persist the trained model with joblib."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)


def main():
    print("=" * 55)
    print("  🌿  GreenMind AI – Energy Model Trainer")
    print("=" * 55)

    print(f"\n📂  Loading dataset from:  {DATA_PATH}")
    df = load_data(DATA_PATH)
    print(f"    Rows: {len(df)}  |  Columns: {list(df.columns)}")

    print("\n🧠  Training RandomForestRegressor (80/20 split) ...")
    model, r2, X_test, y_pred = train(df)

    print(f"\n📊  Model Evaluation:")
    print(f"    R² Score  : {r2:.4f}  ({r2 * 100:.2f}%)")
    print(f"    Test rows : {len(X_test)}")

    if r2 < 0.5:
        print("    ⚠️  Warning: R² is below 0.5. Consider reviewing the data.")
    else:
        print("    ✅  Model accuracy is acceptable.")

    print(f"\n💾  Saving model to: {MODEL_PATH}")
    save_model(model, MODEL_PATH)
    print("    ✅  Model saved successfully.")

    print("\n" + "=" * 55)
    print("  🚀  Next steps:")
    print("  uvicorn api.main:app --reload --port 8000")
    print("  streamlit run app/dashboard.py")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n❌  Dataset Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌  Unexpected error: {e}")
        raise
