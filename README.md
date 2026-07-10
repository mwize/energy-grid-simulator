## Energy Grid Simulator

Interactive Streamlit app for simulating a small energy grid with producers, consumers, weather effects, and a shared battery.

### Features

- Real-time simulation updates (hourly ticks rendered every second)
- Add and remove grid assets from the UI
- Producer assets (e.g., solar, wind, power plant)
- Consumer assets (e.g., household, charging station, factory)
- Battery buffering for surplus/deficit handling
- Live charts for production/consumption and weather trends

### Project Structure

- `/src/main.py` - Streamlit entrypoint
- `/src/controller` - Simulation, weather, and battery logic
- `/src/assets` - Grid asset classes (producers/consumers)
- `/src/pages` - Streamlit dashboard rendering components

### Requirements

- Python 3.14+ (recommended)
- Dependencies listed in `/requirements.txt`

### Installation

```bash
pip install -r requirements.txt
```

### Run the App

From the repository root:

```bash
streamlit run src/main.py
```

Use the version hosted on streamlit

https://energy-grid-simulator.streamlit.app/

### Development Notes

- The app starts with a default `SolarPlant` and `PowerPlant`.
- Simulation state is stored in Streamlit session state.
- Current repository has no automated tests configured.
