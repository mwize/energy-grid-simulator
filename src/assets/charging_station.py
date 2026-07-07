from assets.consumer import Consumer
import random


class ChargingStation(Consumer):
    """Charging station for electric vehicles. Consumes electricity based on a random consumption profile."""

    def __init__(self, asset_id: int = None, priority: int = 0, name: str = "EV Cahrging Station", peak_power_demand: float = 3, max_cars_charging: int = 4):
        self.cars_charging = 0
        self.max_cars_charging = max_cars_charging
        """initializes a charging station with a peak power demand of 2.5 kW."""
        consumption_profile = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        super().__init__(name = name, peak_power_demand = peak_power_demand, consumption_profile = consumption_profile, priority = priority, asset_id = asset_id)

    def consume(self, current_hour) -> float:
        """Returns the consumption of the charging station at a given hour based on random amount of cars charging"""
        random.seed(current_hour)
        self.cars_charging = random.randint(0, self.max_cars_charging)  # Randomly choose number of cars charging (0 to 4)
        return -self.cars_charging * self.peak_power_demand