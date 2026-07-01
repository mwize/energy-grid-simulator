class BatteryController:
    """Encapsulates the central grid battery: charge state and rate limits."""

    def __init__(self, max_kwh: float, max_charge_rate: float, max_discharge_rate: float):
        self.curr_kwh = 0.0
        self.max_kwh = max_kwh
        self.max_charge_rate = max_charge_rate
        self.max_discharge_rate = max_discharge_rate

    def store(self, surplus: float) -> float:
        """Stores surplus energy and returns the amount that did not fit."""
        pass

    def supply(self, deficit: float) -> float:
        """Discharges energy to cover a deficit and returns the uncovered amount."""
        pass