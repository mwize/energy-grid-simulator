import env

class BatteryController:
    """Encapsulates the central grid battery: charge state and rate limits."""

    def __init__(self, curr_kwh = 0.0, max_kwh: float = 10000, max_charge_rate: float = 50, max_discharge_rate: float = 50):
        self.curr_kwh = curr_kwh
        self.max_kwh = max_kwh
        self.max_charge_rate = max_charge_rate
        #should be positive
        self.max_discharge_rate = max_discharge_rate

    def store(self, surplus: float) -> float:
        """Takes net ammount of energy to be stored (positive) or taken from (negative) the battery
        Returns how much energy couldnt be stored (positive), or how much energy could not be taken from the battery"""

        pre_comp = self.curr_kwh

        actual_input = env.clamp(surplus, -self.max_discharge_rate, self.max_charge_rate)
        self.curr_kwh = env.clamp(pre_comp+actual_input, 0, self.max_kwh)
        #calculating diff between pre and post storing operation
        return pre_comp + surplus - self.curr_kwh