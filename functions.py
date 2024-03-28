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