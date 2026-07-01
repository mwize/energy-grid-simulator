from abc import ABC, abstractmethod

from assets.energy_asset import EnergyAsset


class Consumer(EnergyAsset, ABC):
    """Parent class for all power consumers"""

    def __init__(self, name: str, peak_power_demand: float, consumption_profile: list[float], priority: int, asset_id: int):
        """Initializes a consumer with a name, peak power demand, consumption profile, priority, and asset ID."""
        super().__init__(name = name, is_connected = True, asset_id=asset_id)
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

