class Producer:
    """Parent class for all power producers"""

    def __init__(self, name: str, max_capacity: int):
        self.name = name
        self.max_capacity = max_capacity # in kW

    def get_current_capacity(self, weather=None):
        """Returns current power production"""
        raise NotImplementedError("Class must be implemented by Subclass")

