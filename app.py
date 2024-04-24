import streamlit as st
from functions import weather_forecastv2

st.set_page_config(
    page_title="Greenlabel Dashboard",
    page_icon="✅",
    layout="wide",
)   

st.markdown("<h1 style='text-align: center; color: green;'>Greenlabel Dashboard</h1>", unsafe_allow_html=True)

# generate list of cities with lat and long
cities = {
    "Amsterdam, Netherlands": [52.36826475460477, 4.895375012617035],
    "Madrid, Spain": [40.415448970905786, -3.7018545480031992],
    "Paris, France": [48.8566969, 2.3514616],
    "Berlin, Germany": [52.5170365, 13.3888599],
    "Rome, Italy": [41.8933203, 12.4829321],    
}

# weather_forecast("Amsterdam, Netherlands", 52.36826475460477, 4.895375012617035, "Madrid, Spain", 40.415448970905786, -3.7018545480031992)

weather_forecastv2(cities)