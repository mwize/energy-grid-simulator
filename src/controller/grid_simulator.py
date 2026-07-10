from assets.consumer import Consumer
from assets.producer import Producer
import utils as utils

from controller.battery_controller import BatteryController
from controller.weather_controller import WeatherController


class GridSimulator:
    """Orchestrates the simulation over all connected grid members."""

    def __init__(self, weather_controller: WeatherController, battery_controller: BatteryController):
        self.energy_data = (0, 0, 0)  # balance, production, consumption
        self.time_elapsed = 0
        self.grid_members = []
        self.power_history = []
        self.weather_controller = weather_controller
        self.battery_controller = battery_controller

    def add_member(self, asset) -> None:
        """Adds an asset to the grid."""
        self.grid_members.append(asset)

    def remove_member(self, asset_id) -> None:
        """Removes an asset from the grid by its ID."""
        self.grid_members = [a for a in self.grid_members if a.asset_id != asset_id]

    def step(self) -> None:
        """Simulates one time step (one hour)."""

        weather_data = self.weather_controller.get_weather_data(self.time_elapsed)

        self.energy_data = self.update_assets(self.time_elapsed, weather_data)

        # Checks if battery is overloaded
        actual_diff = self.update_battery(self.energy_data[0])
        self.overload_check(actual_diff)

        # Update chart history
        self.update_history(weather_data, self.energy_data)

        # Update time
        self.time_elapsed += 1
    
    def update_assets(self, current_hour: int, weather_data: dict) -> tuple[float, float, float]:
        production = consumption = balance = 0
        for asset in self.grid_members:
            val = asset.update(current_hour, weather_data)
            balance += val
            if val > 0: production += val
            else: consumption += -val
        return balance, production, consumption
    
    def update_history(self, weather_data: dict, energy_data: tuple) -> None:
        """Update chart history."""

        self.power_history.append({
            "Time": self.time_elapsed,
            "production": energy_data[1],
            "consumption": energy_data[2],
            "wind": weather_data["wind_intensity"],
            "sun": weather_data["sun_intensity"],
            "charge": utils.clamp(self.battery_controller.curr_kwh / self.battery_controller.max_kwh, 0 , 1) * 100 if self.battery_controller.curr_kwh > 0 else 0
        })

        # Remove oldest data point if history is too long
        if len(self.power_history) > 50:
            self.power_history.pop(0)

    def update_battery(self, net_balance: float) -> float:
        """Stores surplus or covers a deficit via the battery."""
        return self.battery_controller.store(net_balance)

    def overload_check(self, bal: float) -> None:
        """Checks whether the grid is currently overloaded and turns off all Assets if this is the case"""
        if bal < 0:
            for asset in self.grid_members:
                if isinstance(asset, Consumer):
                    asset.is_connected = False

