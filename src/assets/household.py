from .consumer import Consumer


class HouseHold(Consumer):
    """Houselfold class that consumes energy based on the number of residents and a consumption profile."""

    def __init__(self, asset_id: int = None, num_residents: int = 1, priority: int = 0, name: str = "Household", personal_demand: float = 1.5):
        """initializes a household with a number of residents, a personal demand per resident, and a standard consumption profile."""
        self.num_residents = num_residents
        demand = num_residents * personal_demand
        consumption_profile = [0,0,0,0,0,1,2,2,1,1,1,2,2,1,1,0,1,3,3,2,1,1,1,0]
        super().__init__(name = name, peak_power_demand=demand, consumption_profile=consumption_profile, priority=priority, asset_id=asset_id)

    def consume(self, current_hour) -> float:
        """Returns the consumption of the household at a given hour based on the consumption profile."""
        return -self.consumption_profile[current_hour % 24] * self.num_residents
    