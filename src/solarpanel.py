from .producer import Producer

class SolarPanel(Producer):
    """Produces energy when the sun is shining."""

    def __init__(self, name: str, max_capacity: float):
        super().__init__(name, max_capacity)

    def get_current_capacity(self, weather: float, hour: int) -> float:
        """Returns current power production by solar panel"""

        if 6 <= hour <= 18:
            return weather * self.max_capacity

        return 0