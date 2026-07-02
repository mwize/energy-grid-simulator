from abc import abstractmethod, ABC
import streamlit as st

from assets.energy_asset import EnergyAsset
from assets.household import HouseHold
from assets.powerplant import PowerPlant
from assets.solarplant import SolarPlant
from assets.windturbine import WindTurbine


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
                st.metric("Demand" if kwh < 0 else "Generating", f"{kwh} kwh")

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
    SOLAR_SLIDER_MAX = 100


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
    PP_CAPACITY_SLIDER_MAX = 100

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
            key=self.cap_key
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
    HOUSE_SLIDER_MAX = 100

    def __init__(self, house_asset: HouseHold):
        super().__init__("🏠", house_asset)

        self.pwd_key = f"pwd_sld_{self.asset.asset_id}"  # Key for capacity slider
        self.house_asset = house_asset

    def sync_state(self):
        if self.pwd_key in st.session_state:  # update capacity when slider changed
            self.house_asset.peak_power_demand = st.session_state[self.pwd_key]

    def render_ui_elements(self, weather_data, time):
        # Power Demand slider to change Production
        st.slider(
            "Power Demand",
            min_value=0, max_value=self.HOUSE_SLIDER_MAX,
            value=int(self.house_asset.peak_power_demand),
            key=self.pwd_key
        )


def create_asset_card(asset: EnergyAsset) -> AssetCard:
    """Returns UI card for specific EnergyAsset"""
    if isinstance(asset, SolarPlant):
        return SolarPlantCard(asset)
    elif isinstance(asset, PowerPlant):
        return PowerPlantCard(asset)
    elif isinstance(asset, WindTurbine):
        return WindTurbineCard(asset)
    elif isinstance(asset, HouseHold):
        return HouseHoldCard(asset)
    else:
        raise ValueError(f"No card defined for asset type {type(asset)}")