import streamlit as st
from functions import weather_forecast

st.write("This will be our Green labelling model dashboard:")
    
weather_forecast("Amsterdam, Netherlands", 52.36826475460477, 4.895375012617035)
weather_forecast("Madrid, Spain", 40.415448970905786, -3.7018545480031992)