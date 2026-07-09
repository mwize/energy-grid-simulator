from abc import ABC, abstractmethod

from assets.energy_asset import EnergyAsset


class Producer(EnergyAsset, ABC):
    """Parent class for all power producers"""

    def __init__(self, name: str, max_capacity: float, efficiency: float):
        """Initializes a producer."""
        super().__init__(name = name)
        self.max_capacity = max_capacity # in kW
        self.efficiency = efficiency

    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""

        # Only return power production if asset is connected else zero
        if self.is_connected:
            return self.produce(current_hour, weather_data)
        return 0


    @abstractmethod
    def produce(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""
        pass