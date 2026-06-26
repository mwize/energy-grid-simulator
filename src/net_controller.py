class NetController:
    def __init__(self):
        self.time = 0
        self.day = 0
        weather_data = {
            "cloud_coefficient": .5,
            "wind_coefficient": .5
        }
        self.grid_member = []
        self.bat_curr_kwh = 0
        self.bat_max_kwh = 0

    def step(self):
        pass

    def update_assets(self):
        pass

    def update_battery(self):
        pass

    def overload_check(self):
        pass