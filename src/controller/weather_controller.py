import random
import math
import src.controller.env as env

class WeatherController:
    def __init__(self):
        self.weather_data = {}
        self.sun_inertia = 0.0
        self.sun_intensity = 0.4
        self.wind_intertia = 0.0
        self.wind_intensity = 0.5

    def get_weather_data(self, current_hour: int) -> dict:
        """Returns the weather data for the given hour."""

        #The inertia is tracked to ensure a smooter rate of change in the final weather. Wind params are tweaked to be more volatile than sun
        self.sun_inertia += (random() - 0.5) / 3
        self.wind_intertia += (random() - 0.5) / 1.5

        self.sun_intensity += self.sun_inertia * (0.2 * math.sin(0.7 * current_hour) + 0.5)
        self.wind_intensity += self.wind_intertia * (0.2 * math.sin(1.2 * current_hour) + 0.6)

        self.sun_intensity = env.clamp(self.sun_intensity, 0, 1)
        self.wind_intensity = env.clamp(self.wind_intensity, 0, 1)

        return {"sun_intensity": self.sun_intensity, "wind_intensity": self.wind_intensity}

    