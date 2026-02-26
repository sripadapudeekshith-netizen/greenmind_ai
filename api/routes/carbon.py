"""
Carbon footprint route: POST /api/carbon-footprint
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter
from api.schemas import CarbonInput, CarbonResponse
from models.carbon_estimator import CarbonEstimator

router = APIRouter()
estimator = CarbonEstimator()


@router.post("/carbon-footprint", response_model=CarbonResponse)
def calculate_carbon(inputs: CarbonInput):
    """Calculate annual carbon footprint from lifestyle inputs."""
    result = estimator.estimate(inputs.model_dump())
    return result
