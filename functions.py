import streamlit as st
import pandas as pd
import requests as req

def weather_forecast(city_name, latitude, longitude):
    st.write(f"Weather forecast for {city_name}:")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=sunshine_duration,wind_speed_10m"
    response = req.get(url)
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["date"] = pd.to_datetime(df["time"])
    df["sunshine_duration"] = round(df["sunshine_duration"] / 3600, 1) # convert seconds to hours
    df = df.drop("time", axis=1)
    # change column order
    df = df[["date", "sunshine_duration", "wind_speed_10m"]]
    # group all data by day and calculate the sum of sunshine_duration and the mean of wind_speed_10m
    df = df.resample("D", on="date").agg({"sunshine_duration": "sum", "wind_speed_10m": "mean"}).reset_index()

    # TODO: Change this bar chart because it does not work with the y-axis values
    st.bar_chart(df.set_index("date"))
    st.write(df)