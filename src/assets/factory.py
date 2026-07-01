
from .consumer import Consumer


class Factory(Consumer):
    """Consumes constant energy value"""

    def __init__(self, asset_id: int = None, peak_power_demand: float = 10, priority: int = 0, name: str = "Factory"):
        consumption_profile = [2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2]
        super().__init__(name = name, peak_power_demand = peak_power_demand, consumption_profile = consumption_profile, priority = priority, asset_id = asset_id)

    def consume(self, current_hour)  -> float:
        """"""
        return self.consumption_profile[current_hour] * self.peak_power_demand 



