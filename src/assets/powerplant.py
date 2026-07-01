from assets.producer import Producer


class PowerPlant(Producer):
    """Produces constant energy from fossile energy sources"""

    def __init__(self, max_capacity: float = 20.0, asset_id: int = None, name: str = "Powerplant"):
        """Initializer for PowerPlant. max_capacity asset_id and name is optional"""
        super().__init__(name=name , max_capacity=max_capacity, efficiency=1, asset_id=asset_id)

    def produce(self, current_hour: int, weather_data: dict) -> float:
        """returns produced power based on the max capacity and efficiency, pretty much constant production"""
        return self.max_capacity * self.efficiency