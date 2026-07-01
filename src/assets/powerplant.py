from .producer import Producer


class PowerPlant(Producer):
    """Produces energy from fossile energy sources"""

    def __init__(self, max_capacity: float = 20.0, efficiency: float = 1, asset_id: int = None, name: str = "Powerplant"):
        super().__init__(name , max_capacity, efficiency, asset_id)

    def produce(self, current_hour: int, weather_data: dict) -> float:
        return self.max_capacity * self.efficiency