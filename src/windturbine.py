from src.producer import Producer


class WindTurbine(Producer):
    """Produces energy when the wind is blowing."""

    def __init__(self, max_capacity: float, asset_id: int):
        super().__init__("Wind Turbine", max_capacity, 1, asset_id) # may have to be changed

    def produce(self, current_hour: int, weather_data: dict) -> float:
        pass