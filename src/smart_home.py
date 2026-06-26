from abc import ABC

from .consumer import Consumer
from .producer import Producer


class SmartHome(ABC, Consumer, Producer):
    def __init__(self, num_residents: int):
        self.num_residents = num_residents
    def produce(self, current_hour: int, weather_data: dict) -> float:
        pass
    def consume(self, current_hour: int) -> float:
        pass

    def update(self, current_hour: int, weather_data: dict) -> float:
        pass

    
