from assets.household import HouseHold
from assets.solarplant import SolarPlant

import utils as utils
import math


class SmartHome(HouseHold):
    """A smart home that can both consume and produce energy based on the number of residents, a consumption profile, and solar energy production."""
    def __init__(self, num_residents: int = 1, asset_id: int = None, name = "SmartHome", max_capacity: float = 3, ):
        """initializes a smart home with a number of residents, a personal demand per resident, a standard consumption profile, and a maximum solar energy production capacity (per person)"""
        HouseHold.__init__(self, asset_id = asset_id, num_residents = num_residents, name = name)
        self.solar_panel = SolarPlant(name="SmartHome SolarPanel", max_capacity=max_capacity, asset_id=asset_id)

    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns net energy balance for the smart home"""
        if not self.is_connected:
            return 0
        return self.solar_panel.produce(current_hour, weather_data) + self.consume(current_hour)
