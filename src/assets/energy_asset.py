from abc import ABC, abstractmethod
import random

class EnergyAsset(ABC):
    """
    Base/parent class for all energy assets in the energy grid
    """
    def __init__(self, name: str = "EnergyAsset", is_connected: bool = True, asset_id: int = None):
        #generates a UUID if asset_id is not set
        if not asset_id:
            asset_id = self.generate_uuid()
        self.name = name
        self.is_connected = is_connected
        self.asset_id = asset_id

    def toggle_connect(self):
        """Connects or disconnects the asset from the grid"""
        self.is_connected = not self.is_connected

    @abstractmethod
    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""
        pass

    def generate_uuid(self):
        """Generates a UUID (hopefully)"""
        return random.randrange(999999999)