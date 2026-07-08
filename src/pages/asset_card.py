import math
from abc import abstractmethod, ABC

import pandas as pd
import streamlit as st

from assets.energy_asset import EnergyAsset

from assets.powerplant import PowerPlant
from assets.solarplant import SolarPlant
from assets.windturbine import WindTurbine

from assets.household import HouseHold
from assets.charging_station import ChargingStation
from assets.factory import Factory

from assets.smart_home import SmartHome
from controller.battery_controller import BatteryController


class AssetCard(ABC):
    def __init__(self, icon: str, asset: EnergyAsset):
        self.title = asset.name
        self.icon = icon
        self.asset = asset

    def remove_asset(self):
        st.session_state.grid_simulator.remove_member(self.asset.asset_id)

    def render(self, weather_data, time):
        self.sync_state()

        main_border = st.container(border=True, height=440)

        with main_border:
            title_cols = st.columns([1, 1], gap="small")
            kwh = self.asset.update(time, weather_data)

            with title_cols[0]:
                st.markdown(f"### {self.icon} {self.title}")
            with title_cols[1]:
                st.metric("Demand" if kwh < 0 else "Generating", f"{(kwh**2)**(1/2):.2f} kW")

            st.divider()

            # Render UI elements of specific Asset card
            self.render_ui_elements(weather_data, time)


            button_cols = st.columns([4, 1], gap="small")
            with button_cols[0]:
                btn_label = "🔴 Disconnect" if self.asset.is_connected else "🟢 Connect"
                st.button(btn_label, use_container_width=True, key=f"con_btn_{self.asset.asset_id}", on_click=self.asset.toggle_connect)
            with button_cols[1]:
                st.button("🗑️", use_container_width=True, key=f"rmv_btn_{self.asset.asset_id}", on_click=self.remove_asset)

    @abstractmethod
    def sync_state(self):
        pass

    @abstractmethod
    def render_ui_elements(self, weather_data, time):
        pass



# Asset Card for SolarPlant
class SolarPlantCard(AssetCard):
    # Settings
    SOLAR_SLIDER_MAX = 20


    def __init__(self, solar_asset: SolarPlant):
        super().__init__("☀️", solar_asset)

        self.cap_key = f"cap_sld_{self.asset.asset_id}" # Key for capacity slider
        self.solar_asset = solar_asset

    def sync_state(self):
        if self.cap_key in st.session_state: # update capacity when slider changed
            self.solar_asset.max_capacity = st.session_state[self.cap_key]

    def render_ui_elements(self, weather_data, time):
        # capacity slider to change Production
        st.slider(
            "Capacity",
            min_value=0, max_value=self.SOLAR_SLIDER_MAX,
            value=int(self.solar_asset.max_capacity),
            key=self.cap_key
        )

# Asset Card for Power PowerPlant
class PowerPlantCard(AssetCard):
    # Settings
    PP_CAPACITY_SLIDER_MAX = 40

    def __init__(self, power_asset: PowerPlant):
        super().__init__("🏭", power_asset)
        self.eff_key = f"eff_sld_{self.asset.asset_id}" # Key for efficiency slider
        self.cap_key = f"cap_sld_{self.asset.asset_id}" # Key for capacity slider

        self.power_asset = power_asset

    def sync_state(self):
        # Update efficiency/capacity of power plant when slider changed
        if self.eff_key in st.session_state:
            self.asset.efficiency = st.session_state[self.eff_key]/100
        if self.cap_key in st.session_state:
            self.power_asset.max_capacity = st.session_state[self.cap_key]

    def render_ui_elements(self, weather_data, time):
        # capacity and efficiency sliders
        st.slider(
            "Capacity",
            min_value=0, max_value=self.PP_CAPACITY_SLIDER_MAX,
            value=int(self.power_asset.max_capacity),
            key=self.cap_key,
            step=1
        )

        st.slider(
            "Efficiency (%)",
            min_value=0, max_value=100,
            value=int(self.power_asset.efficiency*100),
            key=self.eff_key
        )

# Asset Card for WindTurbine
class WindTurbineCard(AssetCard):
    # Settings
    WIND_SLIDER_MAX = 100

    def __init__(self, wind_asset: WindTurbine):
        super().__init__("💨", wind_asset)

        self.cap_key = f"cap_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.wind_asset = wind_asset

    def sync_state(self):
        if self.cap_key in st.session_state:  # update capacity when slider changed
            self.wind_asset.max_capacity = st.session_state[self.cap_key]

    def render_ui_elements(self, weather_data, time):
        # capacity slider to change Production
        st.slider(
            "Capacity",
            min_value=0, max_value=self.WIND_SLIDER_MAX,
            value=int(self.wind_asset.max_capacity),
            key=self.cap_key
        )

class HouseHoldCard(AssetCard):
    # Settings
    PER_PERSON_POWER_MAX = 8
    NUM_RESIDENTS_MAX = 10

    def __init__(self, house_asset: HouseHold):
        super().__init__("🏠", house_asset)

        self.pd_key = f"pd_key_{self.asset.asset_id}"  # Key for capacity slider
        self.nr_key = f"nr_key_{self.asset.asset_id}"  # Key for capacity slider
        self.house_asset = house_asset

    def sync_state(self):
        if self.pd_key in st.session_state:  # update capacity when slider changed
            self.house_asset.personal_demand = st.session_state[self.pd_key]
        if self.nr_key in st.session_state:  # update capacity when slider changed
            self.house_asset.num_residents = st.session_state[self.nr_key]

    def render_ui_elements(self, weather_data, time):
        # Power Demand slider to change Production
        st.slider(
            "Base-Demand per Person",
            min_value=0, max_value=self.PER_PERSON_POWER_MAX,
            value=int(self.house_asset.personal_demand),
            key=self.pd_key
        )

        st.slider(
            "Number of Residents",
            min_value=1, max_value=self.NUM_RESIDENTS_MAX,
            value=int(self.house_asset.num_residents),
            key=self.nr_key
        )

class ChargerCard(AssetCard):
    # Settings
    MAX_CARS_SLIDER_MAX = 4
    MAX_POWER_PER_CAR = 6  # kW

    def __init__(self, charger_asset: ChargingStation):
        super().__init__("🔌", charger_asset)

        self.cap_key = f"cap_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.cars_key = f"cars_sld_{self.asset.asset_id}"  # Key for cars slider
        self.charger_asset = charger_asset

    def sync_state(self):
        if self.cap_key in st.session_state:  # update capacity when slider changed
            self.charger_asset.peak_power_demand = st.session_state[self.cap_key]
        if self.cars_key in st.session_state:  # update max cars charging
            self.charger_asset.max_cars_charging = st.session_state[self.cars_key]

    def render_ui_elements(self, weather_data, time):
        # capacity slider to change Production
        st.slider(
            "Max Cars",
            min_value=0, max_value=self.MAX_CARS_SLIDER_MAX,
            value=int(self.charger_asset.max_cars_charging),
            key=self.cars_key
        )

        st.slider(
            "Power per Car (kW)",
            min_value=0, max_value=self.MAX_POWER_PER_CAR,
            value=int(self.charger_asset.peak_power_demand),
            key=self.cap_key
        )
        st.text(f"Current Cars Charging: {self.charger_asset.cars_charging}")


class FactoryCard(AssetCard):
    # Settings
    MAX_PRODUCTION_SLIDER_MAX = 20

    def __init__(self, factory_asset: Factory):
        super().__init__("🏭", factory_asset)

        self.prod_key = f"prod_sld_{self.asset.asset_id}"  # Key for production slider
        self.factory_asset = factory_asset

    def sync_state(self):
        if self.prod_key in st.session_state:  # update production when slider changed
            self.factory_asset.peak_power_demand = st.session_state[self.prod_key]

    def render_ui_elements(self, weather_data, time):
        # production slider to change Production
        st.slider(
            "Production Rate",
            min_value=0, max_value=self.MAX_PRODUCTION_SLIDER_MAX,
            value=int(self.factory_asset.peak_power_demand),
            key=self.prod_key
        )

class SmartHomeCard(AssetCard):
    # Settings
    MAX_RESIDENTS_SLIDER_MAX = 10
    MAX_CAPACITY_SLIDER_MAX = 20

    def __init__(self, smart_home_asset: SmartHome):
        super().__init__("🏡", smart_home_asset)

        self.residents_key = f"res_sld_{self.asset.asset_id}"  # Key for number of residents slider
        self.capacity_key = f"cap_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.smart_home_asset = smart_home_asset

    def sync_state(self):
        if self.residents_key in st.session_state:  # update number of residents when slider changed
            self.smart_home_asset.num_residents = st.session_state[self.residents_key]
        if self.capacity_key in st.session_state:  # update max capacity when slider changed
            self.smart_home_asset.solar_panel.max_capacity = st.session_state[self.capacity_key]

    def render_ui_elements(self, weather_data, time):
        # number of residents slider
        st.slider(
            "Number of Residents",
            min_value=1, max_value=self.MAX_RESIDENTS_SLIDER_MAX,
            value=int(self.smart_home_asset.num_residents),
            key=self.residents_key
        )

        # max capacity slider
        st.slider(
            "Solar Panel Capacity (kW)",
            min_value=0, max_value=self.MAX_CAPACITY_SLIDER_MAX,
            value=int(self.smart_home_asset.solar_panel.max_capacity),
            key=self.capacity_key
        )

class BatteryCard():
    BATTERY_CAPACITY_SLIDER_MAX = 10000

    def __init__(self, battery_controller: BatteryController):
        self.battery_controller = battery_controller

    def sync_state(self):
        if "bat_slider" in st.session_state:  # update number of residents when slider changed

            self.battery_controller.max_kwh = st.session_state["bat_slider"]

    def render(self, weather_data, time):
        self.sync_state()
        main_border = st.container(border=True, height=440)
        with main_border:
            title_cols = st.columns([1, 1], gap="small")
            kwh = self.battery_controller.curr_kwh

            with title_cols[0]:
                st.markdown(f"### 🔋 Battery")
            with title_cols[1]:
                st.metric("Charge", f"{int(kwh)} kWh")

            st.divider()

            df = pd.DataFrame(st.session_state.grid_simulator.power_history).set_index("Time")

            # Chart 1: showing power output over time
            st.area_chart(df[["charge"]], color=["green"], height="stretch")

            # capacity slider to change Production
            st.slider(
                "Capacity",
                min_value=0, max_value=self.BATTERY_CAPACITY_SLIDER_MAX,
                value=int(self.battery_controller.max_kwh),
                key="bat_slider"
            )









def create_asset_card(asset: EnergyAsset) -> AssetCard:
    """Returns UI card for specific EnergyAsset"""
    if isinstance(asset, SmartHome):
        return SmartHomeCard(asset)
    if isinstance(asset, SolarPlant):
        return SolarPlantCard(asset)
    elif isinstance(asset, PowerPlant):
        return PowerPlantCard(asset)
    elif isinstance(asset, WindTurbine):
        return WindTurbineCard(asset)
    elif isinstance(asset, HouseHold):
        return HouseHoldCard(asset)
    elif isinstance(asset, ChargingStation):
        return ChargerCard(asset)
    elif isinstance(asset, Factory):
        return FactoryCard(asset)
    
    else:
        raise ValueError(f"No card defined for asset type {type(asset)}")