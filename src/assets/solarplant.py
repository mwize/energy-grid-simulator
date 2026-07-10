import utils as utils
from assets.producer import Producer
import math

class SolarPlant(Producer):
    """Produces energy when the sun is shining (based on time of day and weather conditions)"""

    def __init__(self, max_capacity: float = 8.0, name: str = "Solar Panel"):
        """Initializer for SolarPanel. max_capacity asset_id and name is optional"""
        super().__init__(name=name, max_capacity=max_capacity, efficiency=1)

    def produce(self, current_hour: int, weather_data: dict) -> float:
        """returns produced power based on the time of day and current weather situation"""

        # Calculate daily solar factor using a shifted sine wave, exponentiated
        # to simulate rapid morning rise/evening drop, then scale by constraints.
        coeffcient = weather_data["sun_intensity"] * self.max_capacity * self.efficiency
        return (utils.clamp((0.6 * math.sin(math.pi / 12 * current_hour - 2) + 0.6), 0, 1) ** 1.5) * coeffcient
