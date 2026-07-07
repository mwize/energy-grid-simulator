import streamlit as st
import pandas as pd

from functools import partial
from assets.energy_asset import EnergyAsset

from assets.household import HouseHold
from assets.charging_station import ChargingStation
from assets.factory import Factory

from assets.solarplant import SolarPlant
from assets.powerplant import PowerPlant
from assets.windturbine import WindTurbine

from assets.smart_home import SmartHome

from pages.asset_card import create_asset_card, BatteryCard


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
            st.button(
                "Solar",
                icon=":material/solar_power:",
                use_container_width=True,
                on_click=partial(add_asset, SolarPlant),
            )


            st.subheader("Consumer")
            st.button(
                "Household",
                icon=":material/house:",
                use_container_width=True,
                on_click=partial(add_asset, HouseHold),
            )
            st.button(
                "Charging Station",
                icon=":material/charger:",
                use_container_width=True,
                on_click=partial(add_asset, ChargingStation),
            )
            st.button(
                "Factory",
                icon=":material/charger:",
                use_container_width=True,
                on_click=partial(add_asset, Factory),
            )


            st.subheader("Other")
            st.button(
                "Smart Home",
                icon=":material/charger:",
                use_container_width=True,
                on_click=partial(add_asset, SmartHome),
            )
            


    # Assets Menu

    with main_cols[1]:
        header_cols = st.columns([6, 2, 1], gap="small") # ratio: Header and time indicatorx
        with header_cols[0]:
            st.title("Assets")
        with header_cols[1]:
            time_string = f"{current_time%24:02d}:00"
            st.metric(label="Time", value=f"{time_string}")
        with header_cols[2]:
            st.metric(label="Days", value=f"{current_time // 24}")

        with st.container(height=760, border=True):
            CARDS_PER_ROW = 3
            grid_cols = st.columns(CARDS_PER_ROW)
            for index, asset in enumerate(assets):
                col_index = index % CARDS_PER_ROW
                with grid_cols[col_index]:
                    card = create_asset_card(asset) if index != 0 else BatteryCard(st.session_state.grid_simulator.battery_controller)

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

            df = pd.DataFrame(st.session_state.grid_simulator.power_history).set_index("Time")

            # Chart 1: showing power output over time
            st.subheader("Power Output")
            st.line_chart(df[["production", "consumption"]], color=["green", "yellow"], height=200)

            # Chart 2: showing weather over time
            st.subheader("Weather")
            st.line_chart(df[["wind", "sun"]], color=["red", "green"], height=200)