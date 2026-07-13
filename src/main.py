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
    """Updates the streamlit interface every second and call step method"""


    st.session_state.grid_simulator.step()

    # Render with the hour and weather that were just simulated, so the UI
    # matches the values in balance, battery and history
    main_screen(
        assets=st.session_state.grid_simulator.grid_members,
        current_time=st.session_state.grid_simulator.last_simulated_hour,
        weather_data=st.session_state.grid_simulator.last_weather
    )


def main():
    """Main function of the app"""

    # Use streamlit wide layout
    st.set_page_config(layout="wide")

    # Create Grid simulator and put it into session state if it doesn't exist
    if "grid_simulator" not in st.session_state:
        st.session_state.grid_simulator = GridSimulator(WeatherController(), BatteryController())

    # Add default Asset Cards
    if not st.session_state.grid_simulator.grid_members:
        st.session_state.grid_simulator.add_member(SolarPlant())
        st.session_state.grid_simulator.add_member(PowerPlant())

    # Inject custom css for more customization of the streamlit ui
    inject_custom_css()

    # start live dashboard and update function
    live_dashboard()


if __name__ == '__main__':
    main()