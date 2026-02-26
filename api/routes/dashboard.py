"""
Dashboard route: GET /api/dashboard/summary
Returns static reference data for populating charts.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter
from api.schemas import DashboardSummary
from data.loader import load_emissions_factors, load_eco_tips

router = APIRouter()


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary():
    """Return global reference data for the dashboard."""
    factors = load_emissions_factors()
    tips = load_eco_tips()
    return {
        "global_average_kg": factors["global_average_annual_kg"],
        "target_kg": factors["target_annual_kg"],
        "uk_average_kg": factors["uk_average_annual_kg"],
        "us_average_kg": factors["us_average_annual_kg"],
        "india_average_kg": factors["india_average_annual_kg"],
        "category_labels": ["Transport", "Energy", "Diet", "Shopping", "Waste"],
        "category_colors": ["#22c55e", "#86efac", "#4ade80", "#16a34a", "#15803d"],
        "tips_count": len(tips),
    }
