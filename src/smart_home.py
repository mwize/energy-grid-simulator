from src.household import HouseHold
from src.producer import Producer


class SmartHome(HouseHold, Producer):
    def __init__(self, num_residents: int, asset_id: int, priority: int):
        HouseHold.__init__(self, asset_id, num_residents, priority)
        Producer.__init__(self, 100, 1, asset_id)
    def produce(self, current_hour: int, weather_data: dict) -> float:
        pass
    def consume(self, current_hour: int) -> float:
        pass

    def update(self, current_hour: int, weather_data: dict) -> float:
        pass

    
