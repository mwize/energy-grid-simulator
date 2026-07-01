
from .consumer import Consumer


class Factory(Consumer):
    """Consumes constant energy value"""

    def __init__(self, asset_id: int, demand: float, priority: int):
        super().__init__("Factory", demand, [demand] * 24, priority, asset_id)

    def consume(self, current_hour)  -> float:
        """"""
        return self.consumption_profile[current_hour]



