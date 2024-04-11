import streamlit as st
from functions import weather_forecast

st.set_page_config(
    page_title="Greenlabel Dashboard",
    page_icon="✅",
    layout="wide",
)    

st.markdown("<h1 style='text-align: center; color: green;'>Greenlabel Dashboard</h1>", unsafe_allow_html=True)



weather_forecast("Amsterdam, Netherlands", 52.36826475460477, 4.895375012617035, "Madrid, Spain", 40.415448970905786, -3.7018545480031992)

