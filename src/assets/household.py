from assets.consumer import Consumer


class Household(Consumer):
    """Household class that consumes energy based on the number of residents and a consumption profile."""

    def __init__(self, num_residents: int = 2, name: str = "Household", personal_demand: float = 1.5):
        """initializes a household with a number of residents, a personal demand per resident, and a consumption profile."""
        self.num_residents = num_residents
        self.personal_demand = personal_demand

        # In the night the power consumption is lower than in the day
        consumption_profile = [0,0,0,0,0,1,2,2,1,1,1,2,2,1,1,0,1,3,3,2,1,1,1,0]
        super().__init__(name=name, peak_power_demand=num_residents*personal_demand, consumption_profile=consumption_profile)

    def consume(self, current_hour) -> float:
        """Returns the consumption of the household at a given hour based on the consumption profile."""

        return -self.consumption_profile[current_hour % 24] * self.personal_demand * self.num_residents
    