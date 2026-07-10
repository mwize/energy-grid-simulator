import streamlit as st
import pandas as pd
from typing import Type
from uuid import UUID

from assets.energy_asset import EnergyAsset

from assets.household import Household
from assets.charging_station import ChargingStation
from assets.factory import Factory

from assets.solarplant import SolarPlant
from assets.powerplant import PowerPlant
from assets.windturbine import WindTurbine

from assets.smart_home import SmartHome

from pages.asset_card import create_asset_card, BatteryCard

PRODUCER_ASSET_BUTTONS = [
    ("Wind Turbine", "wind_power", WindTurbine),
    ("Power Plant", "bolt", PowerPlant),
    ("Solar", "solar_power", SolarPlant),
]

CONSUMER_ASSET_BUTTONS = [
    ("Household", "house", Household),
    ("Charging Station", "charger", ChargingStation),
    ("Factory", "factory", Factory),
]

OTHER_ASSET_BUTTONS = [
    ("Smart Home", "home_health", SmartHome),
]


def main_screen(assets: list[EnergyAsset], current_time: int, weather_data: dict):
    """
    Rendering main screen/dashboard including asset cards
    """
    col_widths = [2, 8, 2] # ratio: Build Menu, Assets, Statistics
    main_cols = st.columns(col_widths)


    # BUILD MENU
    def add_asset(asset_class: Type[EnergyAsset]):
        """creates a new asset and adds it to the grid simulator."""
        new_asset = asset_class()
        st.session_state.grid_simulator.add_member(new_asset)

    def remove_asset(asset_id: UUID):
        """Removes an asset from the grid simulator using the asset_id."""
        st.session_state.grid_simulator.remove_member(asset_id)

    # Show menu buttons to add an asset to the simulation
    with main_cols[0]:
        with st.container(height=110, border=False):    
            st.title("Build Menu")
        with st.container(height=760, border=True):
            st.subheader("Producer")
            for label, icon, cls in PRODUCER_ASSET_BUTTONS:
                st.button(label, icon=f":material/{icon}:", use_container_width=True, on_click=add_asset, args=(cls,))

            st.subheader("Consumer")
            for label, icon, cls in CONSUMER_ASSET_BUTTONS:
                st.button(label, icon=f":material/{icon}:", use_container_width=True, on_click=add_asset, args=(cls,))

            st.subheader("Other")
            for label, icon, cls in OTHER_ASSET_BUTTONS:
                st.button(label, icon=f":material/{icon}:", use_container_width=True, on_click=add_asset, args=(cls,))
            


    # Assets Menu
    with main_cols[1]:
        with st.container(height=110, border=False):
            header_cols = st.columns([6, 2, 1], gap="small") # ratio: Header and time/days
            with header_cols[0]:
                st.title("Assets")
            with header_cols[1]:
                time_string = f"{current_time%24:02d}:00"
                st.metric(label="Time", value=f"{time_string}")
            with header_cols[2]:
                st.metric(label="Days", value=f"{current_time // 24}")

        # Renders each Asset cards for each asset in the simulation
        with st.container(height=760, border=True):
            CARDS_PER_ROW = 3
            grid_cols = st.columns(CARDS_PER_ROW)
            # Render Battery first in first column
            col_index = 0
            with grid_cols[col_index]:
                BatteryCard(st.session_state.grid_simulator.battery_controller).render(
                    weather_data=weather_data, time=current_time
                )

            index = 1

            for asset in assets:
                col_index = index % CARDS_PER_ROW
                with grid_cols[col_index]:
                    card = create_asset_card(asset, on_remove=remove_asset)
                    card.render(weather_data=weather_data, time=current_time)

                index += 1


    # STATISTICS
    with main_cols[2]:
        with st.container(height=110, border=False):
            st.title("Statistics")
        with st.container(height=760, border=True):

            # Total production calculation and visualization
            total_kwh = st.session_state.grid_simulator.energy_data[0]

            st.metric("Current Net-Power", f"{total_kwh:.2f} kW")
            st.divider()

            df = pd.DataFrame(st.session_state.grid_simulator.power_history).set_index("Time")

            # Chart 1: showing power output over time
            st.subheader("Power Output")
            st.line_chart(df[["production", "consumption"]], color=["green", "yellow"], height=200)

            # Chart 2: showing weather over time
            st.subheader("Weather")
            st.line_chart(df[["wind", "sun"]], color=["red", "green"], height=200)