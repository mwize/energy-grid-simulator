from abc import abstractmethod, ABC
from typing import Callable
from uuid import UUID

import pandas as pd
import streamlit as st

from assets.energy_asset import EnergyAsset

from assets.powerplant import PowerPlant
from assets.solarplant import SolarPlant
from assets.windturbine import WindTurbine

from assets.household import Household
from assets.charging_station import ChargingStation
from assets.factory import Factory

from assets.smart_home import SmartHome
from controller.battery_controller import BatteryController


class AssetCard(ABC):
    """Parent class for all asset cards"""
    def __init__(self, icon: str, asset: EnergyAsset, on_remove: Callable[[UUID], None]):
        """Initializes an AssetCard"""
        self.title = asset.name
        self.icon = icon
        self.asset = asset
        self.on_remove = on_remove

    def render(self, weather_data, time):
        """Renders the AssetCard"""

        # Updates asset value when slider is moved
        self.sync_state()

        # AssetCard frame with border
        main_border = st.container(border=True, height=445)
        with main_border:

            # Splits power demand/production metric and title into separate columns to display them next to each other
            title_cols = st.columns([1, 1], gap="small")
            kwh = self.asset.update(time, weather_data)

            with title_cols[0]:
                st.markdown(f"### {self.icon} {self.title}")
            with title_cols[1]:
                # Show Demand/Production metric
                st.metric("Demand" if kwh < 0 else ("Generating" if kwh > 0 else "Idle"), f"{(kwh**2)**(1/2):.2f} kW")

            st.divider()

            # Render UI elements of specific Asset card
            self.render_ui_elements()

            # Add delete and connect buttons
            button_cols = st.columns([4, 1], gap="small")
            with button_cols[0]:
                btn_label = "🔴 Disconnect" if self.asset.is_connected else "🟢 Connect"
                st.button(btn_label, use_container_width=True, key=f"con_btn_{self.asset.asset_id}", on_click=self.asset.toggle_connect)
            with button_cols[1]:
                st.button("🗑️", use_container_width=True, key=f"rmv_btn_{self.asset.asset_id}", on_click=self.on_remove, args=(self.asset.asset_id,))

    @abstractmethod
    def sync_state(self):
        """Updates asset value when slider is moved"""
        pass

    @abstractmethod
    def render_ui_elements(self):
        """Renders UI elements of specific Asset card"""
        pass



# Asset Card for SolarPlant
class SolarPlantCard(AssetCard):
    # Settings
    SOLAR_SLIDER_MAX = 16.0


    def __init__(self, solar_asset: SolarPlant, on_remove: Callable[[UUID], None]):
        super().__init__("☀️", solar_asset, on_remove)

        self.cap_key = f"cap_sld_{self.asset.asset_id}" # Key for capacity slider
        self.solar_asset = solar_asset

    def sync_state(self):
        if self.cap_key in st.session_state: # update capacity when slider changed
            self.solar_asset.max_capacity = st.session_state[self.cap_key]

    def render_ui_elements(self):
        # Slider to change Max capacity of solarplant
        st.slider(
            "Base-Max-Capacity",
            min_value=0.0, max_value=self.SOLAR_SLIDER_MAX,
            value=float(self.solar_asset.max_capacity),
            key=self.cap_key,
            step=0.05
        )

# Asset Card for Power PowerPlant
class PowerPlantCard(AssetCard):
    # Settings
    PP_CAPACITY_SLIDER_MAX = 40.0

    def __init__(self, power_asset: PowerPlant, on_remove: Callable[[UUID], None]):
        super().__init__("⚡", power_asset, on_remove)
        self.eff_key = f"eff_sld_{self.asset.asset_id}" # Key for efficiency slider
        self.cap_key = f"cap_sld_{self.asset.asset_id}" # Key for capacity slider

        self.power_asset = power_asset

    def sync_state(self):
        # Update efficiency/capacity of power plant when slider changed
        if self.eff_key in st.session_state:
            self.asset.efficiency = st.session_state[self.eff_key]/100
        if self.cap_key in st.session_state:
            self.power_asset.max_capacity = st.session_state[self.cap_key]

    def render_ui_elements(self):
        # Slider to change Max capacity of powerplant
        st.slider(
            "Base-Max-Capacity",
            min_value=0.0, max_value=self.PP_CAPACITY_SLIDER_MAX,
            value=float(self.power_asset.max_capacity),
            key=self.cap_key,
            step=0.05
        )

        # Slider to change throttling of powerplant
        st.slider(
            "Throttle (%)",
            min_value=0, max_value=100,
            value=int(self.power_asset.efficiency*100),
            key=self.eff_key
        )

# Asset Card for WindTurbine
class WindTurbineCard(AssetCard):
    # Settings
    WIND_SLIDER_MAX = 15.0

    def __init__(self, wind_asset: WindTurbine, on_remove: Callable[[UUID], None]):
        super().__init__("💨", wind_asset, on_remove)

        self.cap_key = f"cap_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.wind_asset = wind_asset

    def sync_state(self):
        if self.cap_key in st.session_state:  # update capacity when slider changed
            self.wind_asset.max_capacity = st.session_state[self.cap_key]

    def render_ui_elements(self):

        # Slider to change Max capacity of windturbine
        st.slider(
            "Max-Base-Capacity",
            min_value=0.0, max_value=self.WIND_SLIDER_MAX,
            value=float(self.wind_asset.max_capacity),
            key=self.cap_key
        )

class HouseholdCard(AssetCard):
    # Settings
    PER_PERSON_POWER_MAX = 8.0
    NUM_RESIDENTS_MAX = 10

    def __init__(self, house_asset: Household, on_remove: Callable[[UUID], None]):
        super().__init__("🏠", house_asset, on_remove)

        self.pd_key = f"pd_key_{self.asset.asset_id}"  # Key for capacity slider
        self.nr_key = f"nr_key_{self.asset.asset_id}"  # Key for capacity slider
        self.house_asset = house_asset

    def sync_state(self):
        if self.pd_key in st.session_state:  # update capacity when slider changed
            self.house_asset.personal_demand = st.session_state[self.pd_key]
        if self.nr_key in st.session_state:  # update capacity when slider changed
            self.house_asset.num_residents = st.session_state[self.nr_key]

    def render_ui_elements(self):
        # Slider to change personal demand
        st.slider(
            "Base-Demand per Person",
            min_value=0.0, max_value=self.PER_PERSON_POWER_MAX,
            value=float(self.house_asset.personal_demand),
            key=self.pd_key,
            step=0.05
        )

        # Slider to change number of residents
        st.slider(
            "Number of Residents",
            min_value=0, max_value=self.NUM_RESIDENTS_MAX,
            value=int(self.house_asset.num_residents),
            key=self.nr_key
        )

class ChargingStationCard(AssetCard):
    # Settings
    MAX_CARS_SLIDER_MAX = 8
    MAX_POWER_PER_CAR = 6.0  # kW

    def __init__(self, charger_asset: ChargingStation, on_remove: Callable[[UUID], None]):
        super().__init__("🔌", charger_asset, on_remove)

        self.cap_key = f"cap_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.cars_key = f"cars_sld_{self.asset.asset_id}"  # Key for cars slider
        self.charger_asset = charger_asset

    def sync_state(self):
        if self.cap_key in st.session_state:  # update capacity when slider changed
            self.charger_asset.peak_power_demand = st.session_state[self.cap_key]
        if self.cars_key in st.session_state:  # update max cars charging
            self.charger_asset.max_cars_charging = st.session_state[self.cars_key]

    def render_ui_elements(self):

        # Slider to change Max cars charging
        st.slider(
            "Max Cars Amount",
            min_value=0, max_value=self.MAX_CARS_SLIDER_MAX,
            value=int(self.charger_asset.max_cars_charging),
            key=self.cars_key
        )

        # Slider to change Max power per car
        st.slider(
            "Power per Car (kW)",
            min_value=0.0, max_value=self.MAX_POWER_PER_CAR,
            value=float(self.charger_asset.peak_power_demand),
            key=self.cap_key
        )
        st.text(f"Current Cars Charging: {self.charger_asset.cars_charging}")


class FactoryCard(AssetCard):
    # Settings
    MAX_PRODUCTION_SLIDER_MAX = 20.0

    def __init__(self, factory_asset: Factory, on_remove: Callable[[UUID], None]):
        super().__init__("🏭", factory_asset, on_remove)

        self.prod_key = f"prod_sld_{self.asset.asset_id}"  # Key for production slider
        self.factory_asset = factory_asset

    def sync_state(self):
        if self.prod_key in st.session_state:  # update production when slider changed
            self.factory_asset.peak_power_demand = st.session_state[self.prod_key]

    def render_ui_elements(self):
        # Slider to change conveyer belt speed
        st.slider(
            "Conveyor Belt Speed (kW)",
            min_value=0.0, max_value=self.MAX_PRODUCTION_SLIDER_MAX,
            value=float(self.factory_asset.peak_power_demand),
            key=self.prod_key,
            step=0.05
        )

class SmartHomeCard(AssetCard):
    # Settings
    MAX_RESIDENTS_SLIDER_MAX = 8
    MAX_CAPACITY_SLIDER_MAX = 20.0

    def __init__(self, smart_home_asset: SmartHome, on_remove: Callable[[UUID], None]):
        super().__init__("🧠🏠", smart_home_asset, on_remove)

        self.residents_key = f"res_sld_{self.asset.asset_id}"  # Key for number of residents slider
        self.capacity_key = f"cap_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.smart_home_asset = smart_home_asset

    def sync_state(self):
        if self.residents_key in st.session_state:  # update number of residents when slider changed
            self.smart_home_asset.num_residents = st.session_state[self.residents_key]
        if self.capacity_key in st.session_state:  # update max capacity when slider changed
            self.smart_home_asset.solar_panel.max_capacity = st.session_state[self.capacity_key]

    def render_ui_elements(self):
        # Slider to change number of residents
        st.slider(
            "Number of Residents",
            min_value=0, max_value=self.MAX_RESIDENTS_SLIDER_MAX,
            value=int(self.smart_home_asset.num_residents),
            key=self.residents_key
        )

        # Slider to change solar panel base-capacity
        st.slider(
            "Solar Panel Base-Capacity (kW)",
            min_value=0.0, max_value=self.MAX_CAPACITY_SLIDER_MAX,
            value=float(self.smart_home_asset.solar_panel.max_capacity),
            key=self.capacity_key,
            step=0.05
        )

class BatteryCard():
    """Class for creating a default BatteryCard displayed in the first slot"""

    # Settings
    BATTERY_CAPACITY_SLIDER_MAX = 10000

    def __init__(self, battery_controller: BatteryController):
        self.battery_controller = battery_controller

    def sync_state(self):
        """Updates battery max value when slider is moved"""
        if "bat_slider" in st.session_state:  # update number of residents when slider changed

            self.battery_controller.max_kwh = st.session_state["bat_slider"]

    def render(self, weather_data, time):
        """Renders the BatteryCard"""

        self.sync_state()
        main_border = st.container(border=True, height=445)
        with main_border:
            title_cols = st.columns([1, 1], gap="small")
            kwh = self.battery_controller.curr_kwh

            with title_cols[0]:
                st.markdown(f"### 🔋 Battery")
            with title_cols[1]:
                st.metric("Charge", f"{int(kwh)} kWh")

            st.divider()

            df = pd.DataFrame(st.session_state.grid_simulator.power_history).set_index("Time")

            # Chart showing battery charge over time
            st.area_chart(df[["charge"]], color=["green"], height="stretch")

            # Slider to change battery capacity
            st.slider(
                "Max Capacity (kWh)",
                min_value=0, max_value=self.BATTERY_CAPACITY_SLIDER_MAX,
                value=int(self.battery_controller.max_kwh),
                key="bat_slider"
            )


def create_asset_card(asset: EnergyAsset, on_remove: Callable[[UUID], None]) -> AssetCard:
    """Returns UI card for specific EnergyAsset"""
    if isinstance(asset, SmartHome):
        return SmartHomeCard(asset, on_remove)
    if isinstance(asset, SolarPlant):
        return SolarPlantCard(asset, on_remove)
    elif isinstance(asset, PowerPlant):
        return PowerPlantCard(asset, on_remove)
    elif isinstance(asset, WindTurbine):
        return WindTurbineCard(asset, on_remove)
    elif isinstance(asset, Household):
        return HouseholdCard(asset, on_remove)
    elif isinstance(asset, ChargingStation):
        return ChargingStationCard(asset, on_remove)
    elif isinstance(asset, Factory):
        return FactoryCard(asset, on_remove)
    
    else:
        raise ValueError(f"No card defined for asset type {type(asset)}")