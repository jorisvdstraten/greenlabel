import streamlit as st
from functions import weather_forecastv2, calculate_distance, total_penalty

st.set_page_config(
    page_title="Greenlabel Dashboard",
    page_icon="✅",
    layout="wide",
)

# Allow the user to change the value of v on the dashboard
st.sidebar.header('Filters')
energetic_penalty = st.sidebar.slider('Select Transfer Amount (GB)', min_value=0, max_value=999, value=0, step=1)
distance_penalty = st.sidebar.radio("Select Transfer Type", ('wire', 'wireless', 'none'))

st.markdown("<h1 style='text-align: center; color: green;'>Greenlabel Dashboard</h1>", unsafe_allow_html=True)

# Generate list of cities with lat and long
cities = {
    "Amsterdam, Netherlands": [52.36826475460477, 4.895375012617035],
    "Madrid, Spain": [40.415448970905786, -3.7018545480031992],
    "Paris, France": [48.8566969, 2.3514616],
    "Berlin, Germany": [52.5170365, 13.3888599],
    "Rome, Italy": [41.8933203, 12.4829321],    
}

# Get the names of the selected cities from the sidebar
stored_city_name = st.sidebar.selectbox("Select Stored City", list(cities.keys()))
transfer_city_name = st.sidebar.selectbox("Select Transfer City", list(cities.keys()))

# Get the coordinates of the selected cities
stored_city_coordinates = cities[stored_city_name]
transfer_city_coordinates = cities[transfer_city_name]

# Calculate the distance between the selected cities
distance = calculate_distance(stored_city_coordinates, transfer_city_coordinates)

# Calculate the total penalty
total_penalty_value = total_penalty(energetic_penalty, distance_penalty, distance)

# Call the weather_forecastv2 function with the calculated total_penalty_value
weather_forecastv2(cities, energetic_penalty, distance_penalty, total_penalty_value, stored_city_name, transfer_city_name)


