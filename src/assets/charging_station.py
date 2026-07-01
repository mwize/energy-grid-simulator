from .consumer import Consumer


class ChargingStation(Consumer):
    """"""

    def __init__(self, asset_id: int, demand: float, priority: int, name: str, peak_power_demand: float,
                 consumption_profile: list[float]):
        super().__init__(name, peak_power_demand, consumption_profile, priority, asset_id)

    def consume(self, current_hour) -> float:
        """"""
        return self.consumption_profile[current_hour]