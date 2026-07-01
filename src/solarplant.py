from src.producer import Producer

class SolarPlant(Producer):
    """Produces energy when the sun is shining."""

    def __init__(self, max_capacity: float, asset_id: int):
        super().__init__("Solar Panel", max_capacity, 1, asset_id) # may have to be changed

    def produce(self, current_hour: int, weather_data: dict) -> float:
        pass