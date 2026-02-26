"""
Pydantic request/response schemas for the GreenMind AI API.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class CarbonInput(BaseModel):
    transport_mode: str = Field("car_petrol", description="Transport mode key")
    km_per_week: float = Field(100.0, ge=0, description="km driven per week")
    flights_short_per_year: int = Field(0, ge=0, description="Short-haul flights per year")
    flights_long_per_year: int = Field(0, ge=0, description="Long-haul flights per year")
    electricity_kwh_month: float = Field(200.0, ge=0, description="Monthly electricity in kWh")
    natural_gas_kwh_month: float = Field(100.0, ge=0, description="Monthly gas in kWh")
    diet_type: str = Field("meat_medium", description="Diet type")
    clothing_items_per_year: int = Field(10, ge=0, description="Clothing items bought per year")
    electronics_per_year: int = Field(1, ge=0, description="Electronics bought per year")
    waste_recycling_pct: float = Field(30.0, ge=0, le=100, description="Recycling percentage")

    class Config:
        json_schema_extra = {
            "example": {
                "transport_mode": "car_petrol",
                "km_per_week": 200,
                "flights_short_per_year": 2,
                "flights_long_per_year": 1,
                "electricity_kwh_month": 300,
                "natural_gas_kwh_month": 150,
                "diet_type": "meat_medium",
                "clothing_items_per_year": 15,
                "electronics_per_year": 2,
                "waste_recycling_pct": 40,
            }
        }


class CarbonResponse(BaseModel):
    total_kg_co2_year: float
    breakdown: Dict[str, float]
    global_average_kg: float
    target_kg: float
    vs_global_average_pct: float


class ScoreResponse(BaseModel):
    overall_score: float
    grade: str
    grade_label: str
    category_scores: Dict[str, float]
    total_kg_co2_year: float
    breakdown: Dict[str, float]


class TipItem(BaseModel):
    id: int
    category: str
    tip: str
    impact: str
    savings_kg_co2_year: float
    difficulty: str
    tags: List[str]


class TipsResponse(BaseModel):
    tips: List[TipItem]
    count: int


class DashboardSummary(BaseModel):
    global_average_kg: float
    target_kg: float
    uk_average_kg: float
    us_average_kg: float
    india_average_kg: float
    category_labels: List[str]
    category_colors: List[str]
    tips_count: int
