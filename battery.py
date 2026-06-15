class Battery:
    """Can store energy"""

    def __init__(self, capacity: float, current_charge: float,
                 max_charge_rate: float, max_discharge_rate: float, hours_used: int):
        self.capacity = capacity
        self.current_charge = current_charge
        self.max_charge_rate = max_charge_rate
        self.max_discharge_rate = max_discharge_rate



    def charge(self, amount: float) -> float:
        """Charges the battery by a given amount respecting charge rate and capacity"""

        if amount < 0:
            raise ValueError("Charge amount has to be positive")

        available_capacity = self.capacity - self.current_charge

        # Calculates how much energy can be stored in this tick
        actual_charge = min(amount, self.max_charge_rate, available_capacity)
        self.current_charge += actual_charge

        return actual_charge

    def discharge(self, amount: float) -> float:
        """Discharges the battery by a given amount respecting charge rate and capacity"""

        if amount < 0:
            raise ValueError("Discharge amount has to be positive")

        # Calculates how much energy can be discharged in this tick
        actual_discharge = min(amount, self.max_discharge_rate, self.current_charge)
        self.current_charge -= actual_discharge

        return actual_discharge
