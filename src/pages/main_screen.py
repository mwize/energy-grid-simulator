import streamlit as st
import pandas as pd

from assets.energy_asset import EnergyAsset
from pages.asset_card import create_asset_card


def main_screen(assets: list[EnergyAsset], current_time: int, weather_data: dict):
    """
    Rendering main screen/dashboard including asset cards
    """
    col_widths = [2, 8, 2] # ratio: Build Menu, Assets, Statistics
    main_cols = st.columns(col_widths, gap="small")


    # BUILD MENU


    with main_cols[0]:
        st.title("Build Menu")
        with st.container(height=760, border=True):
            st.subheader("Producer")
            st.button("Wind Turbine", icon=":material/wind_power:", use_container_width=True)
            st.button("Power Plant", icon=":material/bolt:", use_container_width=True)

            st.subheader("Consumer")


    # Assets Menu

    with main_cols[1]:
        header_cols = st.columns([3, 1], gap="small") # ratio: Header and time indicator
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
            if "power_history" not in st.session_state:
                st.session_state.power_history = []

            # Add datapoint to power history
            st.session_state.power_history.append({
                "Time": current_time,
                "power": total_kwh
            })

            # Limit power history to 50 ticks
            if len(st.session_state.power_history) > 50:
                st.session_state.power_history.pop(0)  # Delete oldest value

            # Visualize Power Production in line chart
            st.subheader("Power Output")

            df = pd.DataFrame(st.session_state.power_history).set_index("Time")
            st.line_chart(df, color="#2E86C1", height=200)