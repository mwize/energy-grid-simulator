from .weather_controller import WeatherController
from .battery_controller import BatteryController


class GridSimulator:
    """Orchestrates the simulation over all connected grid members."""

    def __init__(self, weather_controller: WeatherController, battery_controller: BatteryController):
        self.time_elapsed = 0
        self.grid_member = []
        self.weather_controller = weather_controller
        self.battery_controller = battery_controller

    def add_member(self, asset) -> None:
        """Adds an asset to the grid."""
        self.grid_member.append(asset)

    def step(self) -> None:
        """Simulates one time step (one hour)."""
        pass

    def update_assets(self, current_hour: int, weather_data: dict) -> float:
        """Calls update() on all members and returns the net balance in kW."""
        pass

    def update_battery(self, net_balance: float) -> None:
        """Stores surplus or covers a deficit via the battery."""
        pass

    def overload_check(self) -> bool:
        """Checks whether the grid is currently overloaded."""
        pass