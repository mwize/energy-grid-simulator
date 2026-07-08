from abc import ABC, abstractmethod
import uuid

class EnergyAsset(ABC):
    """
    Base/parent class for all energy assets in the energy grid
    """

    def __init__(self, name: str = "EnergyAsset", is_connected: bool = True):
        self.name = name
        self.is_connected = is_connected
        self.asset_id = uuid.uuid4()

    def toggle_connect(self):
        """Connects or disconnects EnergyAsset"""
        self.is_connected = not self.is_connected

    @abstractmethod
    def update(self, current_hour: int, weather_data: dict) -> float:
        """Returns current power production"""
        pass
