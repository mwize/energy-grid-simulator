from abc import ABC

from .producer import Producer


class PowerPlant(Producer, ABC):
    """Produces energy from fossile energy sources"""

    def __init__(self, max_capacity: float,efficiency: float, asset_id: int):
        super().__init__("Power Plant", max_capacity, efficiency, asset_id) # may have to be changed

    def produce(self, current_hour: int, weather_data: dict) -> float:
        pass