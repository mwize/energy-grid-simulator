from abc import abstractmethod, ABC
import streamlit as st

from powerplant import PowerPlant
from solarplant import SolarPlant
from energy_asset import EnergyAsset




class AssetCard(ABC):
    def __init__(self, icon: str, asset: EnergyAsset):
        self.title = asset.name
        self.icon = icon
        self.asset = asset

    def remove_asset(self):
        st.session_state.assets = [a for a in st.session_state.assets if a.asset_id != self.asset.asset_id]

    def render(self, weather_data, time):
        self.sync_state()

        main_border = st.container(border=True, height=430)

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





def create_asset_card(asset: EnergyAsset) -> AssetCard:
    """Returns UI card for specific EnergyAsset"""
    if isinstance(asset, SolarPlant):
        return SolarPlantCard(asset)
    elif isinstance(asset, PowerPlant):
        return PowerPlantCard(asset)
    else:
        raise ValueError(f"No card defined for asset type {type(asset)}")