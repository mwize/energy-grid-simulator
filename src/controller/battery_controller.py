import env

class BatteryController:
    """Encapsulates the central grid battery: charge state and rate limits."""

    def __init__(self, curr_kwh = 0.0, max_kwh: float = 10000, max_charge_rate: float = 50, max_discharge_rate: float = 50):
        self.curr_kwh = curr_kwh
        self.max_kwh = max_kwh
        self.max_charge_rate = max_charge_rate
        self.max_discharge_rate = max_discharge_rate

    def store(self, surplus: float) -> float:
        """Stores surplus energy and returns the amount that did not fit."""
        pre_comp = self.curr_kwh

        actual_input = env.clamp(surplus, 0, self.max_charge_rate)
        self.curr_kwh = env.clamp(pre_comp+actual_input, 0, self.max_kwh)
        return pre_comp + surplus - self.curr_kwh

    def supply(self, deficit: float) -> float:
        """Discharges energy to cover a deficit and returns the uncovered amount (negative).
            Takes a negative number!!!"""
        pre_comp = self.curr_kwh
        actual_output = env.clamp(deficit, -self.max_discharge_rate, 0)
        self.curr_kwh = env.clamp(pre_comp + actual_output, 0, self.max_kwh)
        return pre_comp + deficit -self.curr_kwh
    
batt = BatteryController(0, 5, 2, 1)

print(batt.store(1))
print(batt.curr_kwh)

print(batt.supply(-3))
print(batt.curr_kwh)
