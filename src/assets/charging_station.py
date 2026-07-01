from .consumer import Consumer
import random


class ChargingStation(Consumer):
    """"""

    def __init__(self, asset_id: int = None, priority: int = 0, name: str = "EV Cahrging Station", peak_power_demand: float = 2.5):
        consumption_profile = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        super().__init__(name = name, peak_power_demand = peak_power_demand, consumption_profile = consumption_profile, priority = priority, asset_id = asset_id)

    def consume(self, current_hour) -> float:
        """"""
        return random.random(3) * self.peak_power_demand