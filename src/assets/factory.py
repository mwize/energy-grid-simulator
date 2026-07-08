
from assets.consumer import Consumer


class Factory(Consumer):
    """Consumes constant energy value"""

    def __init__(self, asset_id: int = None, peak_power_demand: float = 10, name: str = "Factory"):
        """initializes a factory with a peak power demand of 10 kW."""
        consumption_profile = [2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2]
        super().__init__(name = name, peak_power_demand = peak_power_demand, consumption_profile = consumption_profile, asset_id = asset_id)

    def consume(self, current_hour)  -> float:
        """Returns the consumption of the factory at a given hour based on the consumption profile."""
        return -self.consumption_profile[current_hour % 24] * self.peak_power_demand



