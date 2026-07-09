from assets.consumer import Consumer
from assets.producer import Producer
from controller.battery_controller import BatteryController
from controller.weather_controller import WeatherController


class GridSimulator:
    """Orchestrates the simulation over all connected grid members."""

    def __init__(self, weather_controller: WeatherController, battery_controller: BatteryController):
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

        # calculates current power balance for a given time step and the curreth weather
        balance = self.update_assets(self.time_elapsed, self.weather_controller.get_weather_data(self.time_elapsed))

        # Checks if battery is overloaded
        actual_diff = self.update_battery(balance)
        self.overload_check(actual_diff)

        # Update chart history
        self.update_history()

        # Update time
        self.time_elapsed += 1

    def update_history(self):
        """Update chart history."""

        weather = self.weather_controller.get_weather_data(self.time_elapsed)
        self.power_history.append({
            "Time": self.time_elapsed,
            "production": self.get_production_sum(self.time_elapsed,
                                                  self.weather_controller.get_weather_data(self.time_elapsed)),
            "consumption": self.get_consumption_sum(self.time_elapsed,
                                                    self.weather_controller.get_weather_data(self.time_elapsed)),
            "wind": weather["wind_intensity"],
            "sun": weather["sun_intensity"],
            "charge": (self.battery_controller.curr_kwh / self.battery_controller.max_kwh) * 100 if self.battery_controller.curr_kwh > 0 else 0
        })

        # Remove oldest data point if history is too long
        if len(self.power_history) > 50:
            self.power_history.pop(0)

    def update_assets(self, current_hour: int, weather_data: dict) -> float:
        """Calls update() on all members and returns the net balance in kW."""
        total = 0.0
        for asset in self.grid_members:
            total += asset.update(current_hour, weather_data)
        return total

    def get_production_sum(self, current_hour: int, weather_data: dict) -> float:
        """Returns the sum of all positive (producing) asset outputs at the given hour."""
        total = 0.0
        for asset in self.grid_members:
            value = asset.update(current_hour, weather_data)
            if value > 0:
                total += value
        return total

    def get_consumption_sum(self, current_hour: int, weather_data: dict) -> float:
        """Returns the sum of all negative (consuming) asset outputs at the given hour."""
        total = 0.0
        for asset in self.grid_members:
            value = asset.update(current_hour, weather_data)
            if value < 0:
                total += -value
        return total

    def update_battery(self, net_balance: float) -> float:
        """Stores surplus or covers a deficit via the battery."""
        return self.battery_controller.store(net_balance)

    def overload_check(self, bal: float) -> None:
        """Checks whether the grid is currently overloaded and turns off all Consuming Assets if this is the case"""
        if bal < 0:
            for asset in self.grid_members:
                if isinstance(asset, Consumer):
                    asset.is_connected = False

