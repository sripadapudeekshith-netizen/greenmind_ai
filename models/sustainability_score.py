"""
Sustainability Score Model
Generates a 0–100 sustainability score and letter grade from lifestyle inputs.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.loader import load_emissions_factors


GRADE_THRESHOLDS = [
    (90, "A+", "Exceptional – you're a sustainability champion!"),
    (80, "A",  "Excellent – well above average sustainability."),
    (70, "B",  "Good – you're making a positive impact."),
    (55, "C",  "Average – room for meaningful improvement."),
    (40, "D",  "Below average – consider some key lifestyle changes."),
    (0,  "F",  "Needs work – your footprint is significantly above targets."),
]


class SustainabilityScorer:
    def __init__(self):
        self.factors = load_emissions_factors()

    def score(self, total_kg_co2: float, breakdown: dict) -> dict:
        """
        Score is based on how close total_kg_co2 is to the 2000kg target.
        Breakdown weights are taken into account for category scores.
        """
        target = self.factors["target_annual_kg"]
        worst_case = 20000  # High-consumption profile

        # Overall score (100 = at target or below, 0 = at worst_case or above)
        clamped = max(target, min(worst_case, total_kg_co2))
        raw_score = 100 * (1 - (clamped - target) / (worst_case - target))
        overall = round(max(0, min(100, raw_score)), 1)

        # Category maximums (rough estimates for scoring)
        category_max = {
            "transport": 6000,
            "energy":    3000,
            "diet":      2700,
            "shopping":  1500,
            "waste":     200,
        }
        category_scores = {}
        for cat, val in breakdown.items():
            cat_max = category_max.get(cat, 2000)
            cat_score = 100 * (1 - min(val, cat_max) / cat_max)
            category_scores[cat] = round(max(0, cat_score), 1)

        # Grade
        grade, grade_label = "F", "Needs work – your footprint is significantly above targets."
        for threshold, g, label in GRADE_THRESHOLDS:
            if overall >= threshold:
                grade, grade_label = g, label
                break

        return {
            "overall_score": overall,
            "grade": grade,
            "grade_label": grade_label,
            "category_scores": category_scores,
        }
