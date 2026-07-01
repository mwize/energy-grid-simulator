from .household import HouseHold
from .consumer import Consumer
from .producer import Producer

import src.env
import math


class SmartHome(HouseHold, Producer):
    def __init__(self, num_residents: int = 1, asset_id: int = None, priority: int = 0, name = "SmartHome", max_capacity: float = 3.0, ):
        HouseHold.__init__(self, asset_id, num_residents, priority)
        Producer.__init__(self, name = name, max_capacity = max_capacity, efficiency = 1, asset_id = asset_id)
    def produce(self, current_hour: int, weather_data: dict) -> float:
        
        """returns produced power based on the time of day and current weather situation"""
        return (src.env.clamp((0.6*math.sin(math.pi/12 * current_hour - 2)+0.6), 0 , 1) ** 1.5) * weather_data["sun_intensity"] * self.max_capacity * self.efficiency * self.num_residents
    def update(self, current_hour: int, weather_data: dict) -> float:
        return self.produce(current_hour, weather_data) + self.consume(current_hour)
