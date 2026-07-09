import utils as utils

class BatteryController:
    """Encapsulates the central grid battery: charge state and rate limits."""

    def __init__(self, curr_kwh = 0.0, max_kwh: float = 3000):
        self.curr_kwh = curr_kwh
        self.max_kwh = max_kwh

    def store(self, surplus: float) -> float:
        """Stores surplus energy and returns the leftover amount that exceeded capacity."""

        # Computing the new battery state after storing the surplus energy, clamping it between 0 and max_kwh
        pre_comp = self.curr_kwh
        self.curr_kwh = utils.clamp(pre_comp+surplus, 0, self.max_kwh)

        # calculating diff between pre and post storing operation
        return pre_comp + surplus - self.curr_kwh