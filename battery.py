class Battery:
    """Can store energy"""

    def __init__(self, capacity: float, current_charge: float,
                 max_charge_rate: float, max_discharge_rate: float):
        self.capacity = capacity
        self.current_charge = current_charge
        self.max_charge_rate = max_charge_rate
        self.max_discharge_rate = max_discharge_rate



    def charge(self, amount: float) -> float:
        """Charges the battery by given amount respecting charge rate and capacity"""

        if amount < 0:
            raise ValueError("Charge amount has to be positive")

        available_capacity = self.capacity - self.current_charge

        # Calculates how much energy can be stored in this tick
        actual_charge = min(amount, self.max_charge_rate)
        self.current_charge += actual_charge

        return actual_charge

    def discharge(self, amount: float) -> float:
        pass

    def get_current_charge(self) -> float:
        pass