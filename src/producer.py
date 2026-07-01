from abc import ABC, abstractmethod

from src.energy_asset import EnergyAsset


class Producer(EnergyAsset, ABC):
    """Parent class for all power producers"""

    def __init__(self, name: str, max_capacity: float, efficiency: float, asset_id: int):
        super().__init__(name, True, asset_id)
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