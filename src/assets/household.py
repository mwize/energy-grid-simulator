from .consumer import Consumer


class HouseHold(Consumer):
    """"""

    def __init__(self, asset_id: int, num_residents: int, priority: int):
        self.num_residents = num_residents
        demand = num_residents * 1000 # kW
        consumption_profile = [demand]# tbd
        super().__init__("Household", demand, consumption_profile, priority, asset_id)

    def consume(self, current_hour) -> float:
        """"""
        return self.consumption_profile[current_hour]
