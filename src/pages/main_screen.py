import streamlit as st
import pandas as pd

from functools import partial
from assets.energy_asset import EnergyAsset

from assets.powerplant import PowerPlant
from assets.windturbine import WindTurbine
from pages.asset_card import create_asset_card



def main_screen(assets: list[EnergyAsset], current_time: int, weather_data: dict):
    """
    Rendering main screen/dashboard including asset cards
    """
    col_widths = [2, 8, 2] # ratio: Build Menu, Assets, Statistics
    main_cols = st.columns(col_widths, gap="small")


    # BUILD MENU



    def add_asset(asset_class, *args):
        """Callback: creates a new asset and adds it to the grid simulator."""
        new_asset = asset_class(*args)
        st.session_state.grid_simulator.add_member(new_asset)

    with main_cols[0]:
        st.title("Build Menu")
        with st.container(height=760, border=True):
            st.subheader("Producer")
            st.button(
                "Wind Turbine",
                icon=":material/wind_power:",
                use_container_width=True,
                on_click=partial(add_asset, WindTurbine),
            )
            st.button(
                "Power Plant",
                icon=":material/bolt:",
                use_container_width=True,
                on_click=partial(add_asset, PowerPlant),
            )
            st.subheader("Consumer")


    # Assets Menu

    with main_cols[1]:
        header_cols = st.columns([3, 1], gap="small") # ratio: Header and time indicatorx
        with header_cols[0]:
            st.title("Assets")
        with header_cols[1]:
            st.metric(label="Time", value=f"{current_time}")

        with st.container(height=760, border=True):
            CARDS_PER_ROW = 3
            grid_cols = st.columns(CARDS_PER_ROW)

            for index, asset in enumerate(assets):
                col_index = index % CARDS_PER_ROW
                with grid_cols[col_index]:
                    card = create_asset_card(asset)
                    card.render(weather_data=weather_data, time=current_time)


    # STATISTICS

    with main_cols[2]:
        st.title("Statistics")
        with st.container(height=760, border=True):

            # Total production calculation and visualization
            total_kwh = 0


            for a in assets:
                if a.is_connected:
                    total_kwh += a.update(current_time, weather_data)

            st.metric("Total Power", f"{total_kwh:.2f} kWh")
            st.divider()

            # Initialize power history in session state
            if "power_wind_sun_history" not in st.session_state:
                st.session_state.power_wind_sun_history = []

            # Add datapoint to historic data
            weather = st.session_state.grid_simulator.weather_controller.get_weather_data(current_time)
            st.session_state.power_wind_sun_history.append({
                "Time": current_time,
                "power": total_kwh,
                "wind": weather["wind_intensity"],
                "sun": weather["sun_intensity"]
            })

            # Limit history to 50 ticks
            if len(st.session_state.power_wind_sun_history) > 50:
                # Delete old data
                st.session_state.power_wind_sun_history.pop(0)

            df = pd.DataFrame(st.session_state.power_wind_sun_history).set_index("Time")

            # Chart 1: showing power output over time
            st.subheader("Power Output")
            st.line_chart(df[["power"]], color=["#2E86C1"], height=200)

            # Chart 2: showing weather over time
            st.subheader("Weather")
            st.line_chart(df[["wind", "sun"]], color=["red", "green"], height=200)