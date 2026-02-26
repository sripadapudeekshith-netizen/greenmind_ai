"""
Score route: POST /api/score
Returns sustainability score, grade, and breakdown.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter
from api.schemas import CarbonInput, ScoreResponse
from models.carbon_estimator import CarbonEstimator
from models.sustainability_score import SustainabilityScorer

router = APIRouter()
estimator = CarbonEstimator()
scorer = SustainabilityScorer()


@router.post("/score", response_model=ScoreResponse)
def get_score(inputs: CarbonInput):
    """Calculate sustainability score from lifestyle inputs."""
    carbon_result = estimator.estimate(inputs.model_dump())
    score_result = scorer.score(carbon_result["total_kg_co2_year"], carbon_result["breakdown"])
    return {
        **score_result,
        "total_kg_co2_year": carbon_result["total_kg_co2_year"],
        "breakdown": carbon_result["breakdown"],
    }
