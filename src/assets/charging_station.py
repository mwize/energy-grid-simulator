from assets.consumer import Consumer
import random


class ChargingStation(Consumer):
    """Charging station for electric vehicles. Consumes electricity based on a random consumption profile."""

    def __init__(self, name: str = "EV Charger", peak_power_demand: float = 3, max_cars_charging: int = 4):
        """initializes a charging statio,"""
        self.cars_charging = 0
        self.max_cars_charging = max_cars_charging

        consumption_profile = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        super().__init__(name=name, peak_power_demand=peak_power_demand, consumption_profile=consumption_profile)

    def consume(self, current_hour) -> float:
        random.seed(current_hour)
        # Randomly choose number of cars charging (0 to max_cars_charging(set by slider))
        self.cars_charging = random.randint(0, self.max_cars_charging)
        return -self.cars_charging * self.peak_power_demand * self.consumption_profile[current_hour % 24]