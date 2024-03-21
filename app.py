import streamlit as st
import pandas as pd
import requests as req


def weather_forecast(city_name, latitude, longitude):
    st.write(f"Weather forecast for {city_name}:")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max"
    response = req.get(url)
    data = response.json()
    df = pd.DataFrame(data["daily"])
    df["date"] = pd.to_datetime(df["time"])
    df = df.drop("time", axis=1)
    df = df.rename(columns={"temperature_2m_max": "temperature"})
    # change column order
    df = df[["date", "temperature"]]
    st.bar_chart(df.set_index("date"))
    st.write(df)
# edouard and Lianne and Murphy were here 
weather_forecast("Delfzijl, Netherlands", 53.333950289758135, 6.920911731760793)
weather_forecast("Madrid, Spain", 40.415448970905786, -3.7018545480031992)
weather_forecast("Amsterdam, Netherlands", 52.36826475460477, 4.895375012617035)