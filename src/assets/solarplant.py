from assets.producer import Producer
import math
import src.env

class SolarPlant(Producer):
    """Produces energy when the sun is shining."""

    def __init__(self, max_capacity: float = 8.0 , asset_id: int = None, name: str = "Solar Panel"):
        """Initializer for SolarPanel. max_capacity asset_id and name is optional"""
        super().__init__(name, max_capacity, 1, asset_id)

    def produce(self, current_hour: int, weather_data: dict) -> float:
        """returns produced power based on the time of day and current weather situation"""
        return (src.env.clamp((0.6*math.sin(math.pi/12 * current_hour - 2)+0.6), 0 , 1) ** 1.5) * weather_data["sun_intensity"] * self.max_capacity * self.efficiency
