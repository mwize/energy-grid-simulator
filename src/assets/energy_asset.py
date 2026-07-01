from abc import ABC, abstractmethod
import random

class EnergyAsset(ABC):
    """
    Base/parent class for all energy assets in the energy grid
    """

    _next_id = 0

    @classmethod
    def _generate_id(cls):
        new_id = EnergyAsset._next_id
        EnergyAsset._next_id += 1
        return new_id




    def __init__(self, name: str = "EnergyAsset", is_connected: bool = True, asset_id: int = None):
        #generates a UUID if asset_id is not set
        if not asset_id:
            asset_id = self._generate_id()
        self.name = name
        self.is_connected = is_connected
        self.asset_id = asset_id

    def toggle_connect(self):
        """Connects or disconnects EnergyAsset"""
        self.is_connected = not self.is_connected

    @abstractmethod
    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""
        pass


