from assets.household import HouseHold
from assets.producer import Producer

import src.env
import math


class SmartHome(HouseHold, Producer):
    """A smart home that can both consume and produce energy based on the number of residents, a consumption profile, and solar energy production."""
    def __init__(self, num_residents: int = 1, asset_id: int = None, priority: int = 0, name = "SmartHome", max_capacity: float = 3.0, ):
        """initializes a smart home with a number of residents, a personal demand per resident, a standard consumption profile, and a maximum solar energy production capacity (per person)"""
        HouseHold.__init__(self, asset_id = asset_id, num_residents = num_residents, priority=priority, name = name)
        Producer.__init__(self, name = name, max_capacity = max_capacity, efficiency = 1, asset_id = asset_id)

    def produce(self, current_hour: int, weather_data: dict) -> float:
        """returns produced power based on the time of day and current weather situation"""
        return (src.env.clamp((0.6*math.sin(math.pi/12 * current_hour - 2)+0.6), 0 , 1) ** 1.5) * weather_data["sun_intensity"] * self.max_capacity * self.efficiency * self.num_residents
    
    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns net energy balance for the smart home"""
        if not self.is_connected:
            return 0
        return self.produce(current_hour, weather_data) + self.consume(current_hour)
