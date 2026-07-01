import streamlit as st

from assets.energy_asset import EnergyAsset
from assets.powerplant import PowerPlant
from assets.solarplant import SolarPlant
from controller.weather_controller import WeatherController
from controller.battery_controller import BatteryController
from controller.grid_simulator import GridSimulator
from pages.main_screen import main_screen
from pages.utils.styling_utils import inject_custom_css


@st.fragment(run_every=1)
def live_dashboard():
    st.session_state.grid_simulator.step()
    main_screen(
        assets=st.session_state.grid_simulator.grid_members,
        current_time=st.session_state.grid_simulator.time_elapsed,
        weather_data=st.session_state.grid_simulator.weather_controller.get_weather_data(
            st.session_state.grid_simulator.time_elapsed
        )
    )

def main():
    if "grid_simulator" not in st.session_state:
        st.session_state.grid_simulator = GridSimulator(WeatherController(), BatteryController())
    st.set_page_config(layout="wide")
    inject_custom_css()
    if not st.session_state.grid_simulator.grid_members:
        st.session_state.grid_simulator.add_member(SolarPlant(EnergyAsset._generate_id()))
        st.session_state.grid_simulator.add_member(PowerPlant(EnergyAsset._generate_id()))

    if "sim_time" not in st.session_state:
        st.session_state.sim_time = 0
    live_dashboard()


if __name__ == '__main__':
    main()