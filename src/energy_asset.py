class EnergyAsset:
    """
    Base/parent class for all energy assets in the energy grid
    """
    def __init__(self, name: str):
        self.name = name