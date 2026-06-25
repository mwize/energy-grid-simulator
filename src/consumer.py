from abc import ABC, abstractmethod

from energy_asset import EnergyAsset


class Consumer(ABC, EnergyAsset):
    """Parent class for all power consumers"""

    def __init__(self, name: str, peak_power_demand: float, consumption_profile: list[float], priority: int, asset_id: int):
        super().__init__(name, True, asset_id)
        self.peak_power_demand = peak_power_demand
        self.consumption_profile = consumption_profile
        self.priority = priority

    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power consumption"""
        if self.is_connected:
            return self.consume(current_hour)
        return 0

    @abstractmethod
    def consume(self, current_hour: int) -> float:
        """Returns current power consumption"""
        pass

