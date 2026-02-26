import json
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def load_emissions_factors() -> dict:
    path = os.path.join(DATA_DIR, "emissions_factors.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_eco_tips() -> list:
    path = os.path.join(DATA_DIR, "eco_tips.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
