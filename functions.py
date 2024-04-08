
#This library is to create interactive web applications for machine learning and data science  
import streamlit as st

#This library is to provides data structures and data analysis tools
import pandas as pd
        
#This library simplifies HTTP requests, allowing to interact with APIs easily
import requests as req


def weather_forecast(city_name, latitude, longitude):

     #Display "Weather forecast for" and give the name of the city choosen in app.py
    st.write(f"Weather forecast for {city_name}:") 

    #Create the API URL to collectec data from open-meteo.com 
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=sunshine_duration,wind_speed_10m"

    #request the url 
    response = req.get(url)

    # Convert the response to JSON format
    data = response.json()

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data["hourly"])

    #change the format of the column to date time format 
    df["date"] = pd.to_datetime(df["time"])

    # convert seconds to hours
    df["sunshine_duration"] = round(df["sunshine_duration"] / 3600, 1)

    # Drop the 'time' columna
    df = df.drop("time", axis=1)


    # change column order
    df = df[["date", "sunshine_duration", "wind_speed_10m"]]

    # group all data by day and calculate the sum of sunshine_duration and the mean of wind_speed_10m
    df = df.resample("D", on="date").agg({"sunshine_duration": "sum", "wind_speed_10m": "mean"}).reset_index()

    # TODO: Change this bar chart because it does not work with the y-axis values
    st.bar_chart(df.set_index("date"))
    st.write(df)