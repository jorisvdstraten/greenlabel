
import streamlit as st

#Import the function weather_forecast that we created from function
from functions import weather_forecast

#Display text on the top of the dashboard created 
st.write("This will be our Green labelling model dashboard:")

#import and use the function weather_forecast that have been created. Use it for Amsterdam city.   
weather_forecast("Amsterdam, Netherlands", 52.36826475460477, 4.895375012617035)

#import and use the function weather_forecast that have been created. Use it for Madrid city. 
weather_forecast("Madrid, Spain", 40.415448970905786, -3.7018545480031992)