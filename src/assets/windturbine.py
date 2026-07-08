from assets.producer import Producer
import math

class WindTurbine(Producer):
    """Produces energy when the wind is blowing."""

    def __init__(self, max_capacity: float = 5.0, asset_id: int = None, name: str = "Wind Turbine"):
        """Initializer for WindTurbine. max_capacity, asset_id and name is optional"""
        super().__init__(name=name, max_capacity=max_capacity, efficiency=1, asset_id=asset_id)

    def produce(self, current_hour: int, weather_data: dict) -> float:
        """Returns produced power based on current 'season' (0.1*current_hour) and current weather situation """
        return (0.2 * math.sin(0.1*current_hour) + 0.8) * weather_data["wind_intensity"] * self.efficiency*self.max_capacity