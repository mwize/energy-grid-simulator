from abc import ABC

from .consumer import Consumer


class ChargingStation(Consumer, ABC):
    """"""

    def __init__(self, asset_id: int, demand: float, priority: int):
        pass

    def consume(self, current_hour) -> float:
        """"""
        return self.consumption_profile[current_hour]