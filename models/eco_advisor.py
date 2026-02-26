"""
Eco Advisor
Returns personalised eco-tips based on the user's highest-impact categories.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.loader import load_eco_tips


class EcoAdvisor:
    def __init__(self):
        self.tips = load_eco_tips()

    def recommend(self, breakdown: dict, top_n: int = 5) -> list:
        """
        Recommend tips targeting the user's highest-emission categories.

        breakdown: dict of {category: kg_co2_year}
        Returns a list of tip dicts sorted by relevance + impact.
        """
        # Sort categories by emission descending
        sorted_cats = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        priority_cats = [cat for cat, _ in sorted_cats]

        scored_tips = []
        for tip in self.tips:
            cat = tip.get("category", "")
            impact = tip.get("impact", "low")
            impact_weight = {"high": 3, "medium": 2, "low": 1}.get(impact, 1)

            # Priority: appear in top-emission categories
            try:
                cat_rank = priority_cats.index(cat)
            except ValueError:
                cat_rank = len(priority_cats)

            relevance = (len(priority_cats) - cat_rank) * impact_weight
            scored_tips.append((relevance, tip))

        scored_tips.sort(key=lambda x: x[0], reverse=True)
        return [tip for _, tip in scored_tips[:top_n]]

    def get_by_category(self, category: str) -> list:
        return [t for t in self.tips if t["category"] == category]

    def get_all(self) -> list:
        return self.tips
