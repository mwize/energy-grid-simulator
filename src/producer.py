from .energy_asset import EnergyAsset


class Producer(EnergyAsset):
    """Parent class for all power producers"""

    def __init__(self, name: str, max_capacity: float):
        super().__init__(name)
        self.max_capacity = max_capacity # in kW

    def get_current_capacity(self, weather: float, hour: int) -> float:
        """Returns current power production"""
        raise NotImplementedError("Class must be implemented by Subclass")

