"""
Tips route: GET /api/tips
Returns personalized eco-tips, optionally filtered by category.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter, Query
from typing import Optional
from api.schemas import TipsResponse
from models.eco_advisor import EcoAdvisor

router = APIRouter()
advisor = EcoAdvisor()


@router.get("/tips", response_model=TipsResponse)
def get_tips(
    category: Optional[str] = Query(None, description="Filter by category: transport|energy|diet|shopping|waste"),
    limit: int = Query(10, ge=1, le=50, description="Max number of tips to return"),
):
    """Get eco-tips, optionally filtered by category."""
    if category:
        tips = advisor.get_by_category(category)[:limit]
    else:
        tips = advisor.get_all()[:limit]
    return {"tips": tips, "count": len(tips)}
