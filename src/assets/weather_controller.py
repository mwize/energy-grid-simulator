class WeatherController:
    """Generates and stores the current weather state of the simulation."""

    def __init__(self):
        self.weather_data = {
            "cloud_coefficient": 0.5,
            "wind_coefficient": 0.5,
        }


    def get_weather(self) -> dict:
        """Returns the current weather data."""
        return self.weather_data