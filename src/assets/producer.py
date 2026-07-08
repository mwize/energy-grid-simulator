from abc import ABC, abstractmethod

from assets.energy_asset import EnergyAsset


class Producer(EnergyAsset, ABC):
    """Parent class for all power producers"""

    def __init__(self, name: str, max_capacity: int, efficiency: float):
        super().__init__(name = name, is_connected=True)
        self.max_capacity = max_capacity # in kW
        self.efficiency = efficiency

    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""
        if self.is_connected:
            return self.produce(current_hour, weather_data)
        return 0


    @abstractmethod
    def produce(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""
        pass