from controller.battery_controller import BatteryController
from controller.weather_controller import WeatherController


class GridSimulator:
    """Orchestrates the simulation over all connected grid members."""

    def __init__(self, weather_controller: WeatherController, battery_controller: BatteryController):
        self.time_elapsed = 0
        self.grid_members = []
        self.weather_controller = weather_controller
        self.battery_controller = battery_controller

    def add_member(self, asset) -> None:
        """Adds an asset to the grid."""
        self.grid_members.append(asset)

    def step(self) -> None:
        """Simulates one time step (one hour)."""
        balance = self.update_assets(self.time_elapsed, self.weather_controller.get_weather_data(self.time_elapsed))
        actual_diff = self.update_battery(balance)
        self.overload_check(actual_diff)
        
        self.time_elapsed += 1
        pass

    def update_assets(self, current_hour: int, weather_data: dict) -> float:
        """Calls update() on all members and returns the net balance in kW."""
        total = 0.0
        for asset in self.grid_members:
            total += asset.update(current_hour, weather_data)
        return total

    def update_battery(self, net_balance: float) -> float:
        """Stores surplus or covers a deficit via the battery."""
        return self.battery_controller.store(net_balance)

    def overload_check(self, bal: float) -> bool:
        """Checks whether the grid is currently overloaded and turns off all Assets if this is the case"""
        if bal < 0:
            for asset in self.grid_members:
                asset.is_connected = False

    def remove_member(self, asset_id) -> None:
        """Removes an asset from the grid by its ID."""
        self.grid_members = [a for a in self.grid_members if a.asset_id != asset_id]