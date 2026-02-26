"""
Carbon Footprint Estimator
Estimates annual CO2 equivalent emissions (kg/year) from user lifestyle inputs.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.loader import load_emissions_factors


class CarbonEstimator:
    def __init__(self):
        self.factors = load_emissions_factors()

    def estimate(self, inputs: dict) -> dict:
        """
        Estimate carbon footprint from user inputs.

        inputs dict keys:
          transport_mode: str  (car_petrol|car_diesel|car_electric|bus|train|motorcycle|bicycle|walking)
          km_per_week: float
          flights_short_per_year: int
          flights_long_per_year: int
          electricity_kwh_month: float
          natural_gas_kwh_month: float
          diet_type: str  (meat_heavy|meat_medium|pescatarian|vegetarian|vegan)
          clothing_items_per_year: int
          electronics_per_year: int
          waste_recycling_pct: float  (0-100)
        """
        factors = self.factors
        breakdown = {}

        # --- Transport ---
        mode = inputs.get("transport_mode", "car_petrol")
        km_week = float(inputs.get("km_per_week", 0))
        km_year = km_week * 52
        transport_key = f"{mode}_km"
        transport_factor = factors["transport"].get(transport_key, factors["transport"]["car_petrol_km"])
        transport_co2 = km_year * transport_factor

        # Flights
        short_flights = int(inputs.get("flights_short_per_year", 0))
        long_flights = int(inputs.get("flights_long_per_year", 0))
        avg_short_km = 800
        avg_long_km = 5000
        flight_co2 = (
            short_flights * avg_short_km * factors["transport"]["flight_short_km"] +
            long_flights * avg_long_km * factors["transport"]["flight_long_km"]
        )
        breakdown["transport"] = round(transport_co2 + flight_co2, 1)

        # --- Energy ---
        elec_kwh_month = float(inputs.get("electricity_kwh_month", 200))
        gas_kwh_month = float(inputs.get("natural_gas_kwh_month", 100))
        elec_co2 = elec_kwh_month * 12 * factors["energy"]["electricity_kwh"]
        gas_co2 = gas_kwh_month * 12 * factors["energy"]["natural_gas_kwh"]
        breakdown["energy"] = round(elec_co2 + gas_co2, 1)

        # --- Diet ---
        diet = inputs.get("diet_type", "meat_medium")
        diet_key = f"{diet}_daily_kg_co2"
        diet_factor = factors["diet"].get(diet_key, factors["diet"]["meat_medium_daily_kg_co2"])
        breakdown["diet"] = round(diet_factor * 365, 1)

        # --- Shopping ---
        clothing = int(inputs.get("clothing_items_per_year", 10))
        electronics = int(inputs.get("electronics_per_year", 1))
        shopping_co2 = (
            clothing * factors["shopping"]["clothing_item"] +
            electronics * factors["shopping"]["electronics_device"]
        )
        breakdown["shopping"] = round(shopping_co2, 1)

        # --- Waste ---
        recycling_pct = float(inputs.get("waste_recycling_pct", 30)) / 100
        avg_waste_kg_week = 7  # average household
        waste_kg_year = avg_waste_kg_week * 52
        recycled = waste_kg_year * recycling_pct
        landfill = waste_kg_year * (1 - recycling_pct)
        waste_co2 = (
            landfill * factors["waste"]["landfill_kg"] +
            recycled * factors["waste"]["recycled_kg"]
        )
        breakdown["waste"] = round(waste_co2, 1)

        total = sum(breakdown.values())

        return {
            "total_kg_co2_year": round(total, 1),
            "breakdown": breakdown,
            "global_average_kg": factors["global_average_annual_kg"],
            "target_kg": factors["target_annual_kg"],
            "vs_global_average_pct": round(((total - factors["global_average_annual_kg"]) / factors["global_average_annual_kg"]) * 100, 1),
        }
