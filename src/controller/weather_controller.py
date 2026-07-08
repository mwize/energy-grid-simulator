import random
import math
import utils as utils


class WeatherController:
    """Generates weather data based on simple sine curves with a bit of random noise."""

    # How much random noise is mixed into the sine curve (0 = none, 1 = a lot)
    SUN_NOISE = 0.5
    WIND_NOISE = 0.85

    # How quickly the noise is allowed to change from hour to hour (smoothing)
    NOISE_SMOOTHING = 0.3

    def __init__(self):
        self.weather_data = {}   # Cache: hour -> weather dict
        self.sun_noise = 0.0
        self.wind_noise = 0.0

    def get_weather_data(self, current_hour: int) -> dict:
        """Returns the weather data for the given hour."""

        # Return cached value if this hour was already computed, so repeated
        # calls within the same hour (e.g. from grid_simulator.step()) stay consistent
        if current_hour in self.weather_data:
            return self.weather_data[current_hour]

        # Base curve: sun follows a 24h day/night cycle, wind a slightly different rhythm
        sun_base = 0.5 + 0.5 * math.sin((2 * math.pi / 24) * current_hour - math.pi / 2)
        wind_base = 0.5 + 0.3 * math.sin((2 * math.pi / 36) * current_hour)

        # Smoothly nudge the noise toward a new random value instead of jumping around
        self.sun_noise += self.NOISE_SMOOTHING * ((random.random() - 0.5) - self.sun_noise)
        self.wind_noise += self.NOISE_SMOOTHING * ((random.random() - 0.5) - self.wind_noise)

        sun_intensity = utils.clamp(sun_base + self.sun_noise * self.SUN_NOISE, 0, 1)
        wind_intensity = utils.clamp(wind_base + self.wind_noise * self.WIND_NOISE, 0, 1)

        result = {"sun_intensity": sun_intensity, "wind_intensity": wind_intensity}
        self.weather_data[current_hour] = result

        # Keep cache small, mirroring power_history in grid_simulator.py
        if len(self.weather_data) > 50:
            oldest = min(self.weather_data)
            del self.weather_data[oldest]

        return result
