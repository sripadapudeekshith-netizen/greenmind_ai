"""
GreenMind AI – FastAPI Backend
Provides energy usage prediction via a trained RandomForest model.

Endpoints:
    GET  /          → Health check
    POST /predict   → Energy prediction (kWh)
    GET  /docs      → Swagger UI (auto-generated)
"""

import os
import sys
from contextlib import asynccontextmanager

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# Ensure stdout can handle utf-8 characters properly on Windows
sys.stdout.reconfigure(encoding='utf-8')

# ── Paths ───────────────────────────────────────────────────────────────────
ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, "models", "energy_model.pkl")

# ── Model loader ─────────────────────────────────────────────────────────────
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model on startup; release on shutdown."""
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print(f"✅  Model loaded from: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    else:
        # On Vercel, the path might be slightly different or the model might not exist if not trained
        print(f"⚠️  Model not found at '{MODEL_PATH}'.")
    yield
    model = None


# Ensure model is checked before each prediction if lifespan hasn't run fully or for simplicity in serverless
def get_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
    return model


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="GreenMind AI – Energy API",
    description=(
        "Smart Energy Optimization API. "
        "Predicts energy consumption based on temperature, humidity, and hour."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS (allow Streamlit + Render frontends) ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schemas ──────────────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    temperature: float = Field(..., ge=0, le=60, description="Temperature in °C (0–60)")
    humidity: float    = Field(..., ge=0, le=100, description="Relative humidity in % (0–100)")
    hour: int          = Field(..., ge=0, le=23, description="Hour of day (0–23)")

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v):
        if not (0 <= v <= 60):
            raise ValueError("temperature must be between 0 and 60 °C.")
        return v

    @field_validator("humidity")
    @classmethod
    def validate_humidity(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("humidity must be between 0 and 100 %.")
        return v

    @field_validator("hour")
    @classmethod
    def validate_hour(cls, v):
        if not (0 <= v <= 23):
            raise ValueError("hour must be between 0 and 23.")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "temperature": 32.5,
                "humidity": 60,
                "hour": 14,
            }
        }
    }


class PredictResponse(BaseModel):
    predicted_energy: float
    unit: str = "kWh"


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "GreenMind AI API Running"}


@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
def predict(data: PredictRequest):
    """
    Predict energy usage in kWh given temperature, humidity, and hour.
    Returns the predicted value and unit.
    """
    current_model = get_model()
    if current_model is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "ML model is not loaded. "
                "Please run 'python models/train.py' to train and save the model."
            ),
        )

    try:
        features = np.array([[data.temperature, data.humidity, data.hour]])
        prediction = current_model.predict(features)[0]
        predicted_energy = round(float(prediction), 4)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed due to an internal error: {exc}",
        )

    return PredictResponse(predicted_energy=predicted_energy)
