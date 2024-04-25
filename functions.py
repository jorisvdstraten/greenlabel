import streamlit as st
import pandas as pd
import requests as req
import altair as alt
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from geopy.distance import geodesic

 
# Variables for the model
P = 2250 # Define the values of the fixed variables for the energy calculation
Cp = 0.6  
Cf = 0.3  
a = 20  # amount of wind turbines / wind mills
 
y = 325
q = 0.8
n = 100 # amount of solar panels
 
v = 1.008
enegetic_penalty = 10 # The energetic penalty is 1 Kwh for 100 GB
 
# Written by Eduoard 
def calculate_distance(city1, city2) -> float:
    return geodesic(city1, city2).kilometers
    #   st.sidebar.write(f"Distance between {actual_city} and {next_city}: {distance:.2f} km")

def fetch_weather_data(city_name, latitude, longitude): # Function to fetch and process weather data
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=sunshine_duration,wind_speed_10m"
    response = req.get(url)
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["date"] = pd.to_datetime(df["time"]).dt.date
    df["sunshine_duration"] = round(df["sunshine_duration"] / 3600, 1)
    df["wind_speed_10m"] = df["wind_speed_10m"].round(1)
    df = df.drop("time", axis=1)
    df = df.groupby("date").agg({"sunshine_duration": "sum", "wind_speed_10m": "mean"}).reset_index()
 
    return df
 
def weather_forecastv2(cities):
    dfAll = pd.DataFrame()
    # iterate over the cities and append df to dfAll
    for city, coordinates in cities.items():
        df = fetch_weather_data(city, coordinates[0], coordinates[1])
        df["city"] = city
        dfAll = pd.concat([dfAll, df])
 
    # calculate E(w) based on the provided equation
    dfAll = dfAll.assign(Ew = lambda x: v * a * x['wind_speed_10m'])
    # calculate E(s) based on the provided equation
    dfAll = dfAll.assign(Es = lambda x: y * x['sunshine_duration'] * q * n / 1000)
    # calculate total green energy
    dfAll = dfAll.assign(Total_green_energy = lambda x: x['Ew'] + x['Es'])
 
    # Group by 'date' to find the maximum energy per date across all cities
    grouped = dfAll.groupby('date')
    max_energy_per_date = grouped['Total_green_energy'].transform('max')
 
    # Create a new column 'Most_energy_generated' that shows the maximum energy value for each date
    dfAll['Most_energy_generated'] = max_energy_per_date
 
    # Determine the city associated with the maximum energy value for each date
    # First, create a mask to identify rows where 'Total_green_energy' matches 'Most_energy_generated'
    mask = dfAll['Total_green_energy'] == dfAll['Most_energy_generated']
 
    # Use the mask to filter rows and retrieve the corresponding city names
    max_city_per_date = dfAll.loc[mask, ['date', 'city']]
 
    # Merge the city names back into the original DataFrame based on 'date'
    dfAll = dfAll.merge(max_city_per_date, on='date', suffixes=('', '_max_city'))
 
    # Rename the columns to reflect the maximum city name
    dfAll.rename(columns={'city_max_city': 'City_most_energy_generated / label'}, inplace=True)
 
    # show the dfAll
    # st.write(dfAll)
 
 
    # Sidebar for selecting locations
    st.sidebar.header('Filters')
    all_dates = ['All'] + list(dfAll['date'].unique())
    all_locations = ['All'] + list(cities.keys())
    stored_location = st.sidebar.selectbox("Stored Location", list(cities.keys()))
    location = st.sidebar.selectbox("Location", list(cities.keys()))
    selected_date = st.sidebar.selectbox("Date", dfAll['date'].unique())
  
    # Button 1: Filters information
    if st.sidebar.button('ℹ️ Filters'):
        st.sidebar.write("""
        The 'Stored Location' is the location where the data is currently stored.
                         
        The 'Location' is the location that you want to transfer the data to.
                         
        The 'Date' is the date you want to compare the cities for transfer.           
    """)
    
    # Button 2: Labels information
    if st.sidebar.button('ℹ️ Labels'):
         st.sidebar.write("""  
        If the label is 'Green' the transfer is beneficial.
                         
        If the label is 'Orange' the transfer could be beneficial.
                         
        If the label is 'Red' the transfer is not beneficial.             
    """)
 
    # Filter DataFrame based on selected locations
    stored_location_df = dfAll[(dfAll['city'] == stored_location) & (dfAll['date'] == selected_date)]
    location_df = dfAll[(dfAll['city'] == location) & (dfAll['date'] == selected_date)]
 
    # Calculate the difference in total_green_energy between selected locations
    stored_energy = stored_location_df['Total_green_energy'].sum()
    location_energy = location_df['Total_green_energy'].sum()
    energy_difference = location_energy - stored_energy
 
    # Determine label based on energy difference value
    def get_label(energy_difference):
        if energy_difference > 100:
            return 'Green', 'Green'
        elif -100 <= energy_difference <= 100:
            return 'Orange', 'Orange'
        else:
            return 'Red', 'Red'
 
    # Calculate label based on energy difference
    label_color, energy_label = get_label(energy_difference)
 
    # Display the energy difference label on top of the dashboard
    st.markdown(f'<p style="color:{label_color}; font-size:20px;"> Label: {energy_label} </p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{label_color}; font-size:20px;"> Date: {selected_date} </p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{label_color}; font-size:20px;"> Difference: {energy_difference:.2f} Kwh </p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{label_color}; font-size:20px;"> From: {stored_location} </p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{label_color}; font-size:20px;"> To: {location} </p>', unsafe_allow_html=True)

   
    # plot a bar chart side by side for wind speed using plotly
    fig = px.bar(location_df, x='date', y='wind_speed_10m', color='city', barmode='group')
    fig3 = px.bar(stored_location_df, x='date', y='wind_speed_10m', color='city', barmode='group')
 
    # # plot a bar chart side by side for sunshine using plotly
    fig2 = px.bar(location_df, x='date', y='sunshine_duration', color='city', barmode='group')
    fig4 = px.bar(stored_location_df, x='date', y='sunshine_duration', color='city', barmode='group')
 
    #col1, col2 = st.columns(2)
    #with col1:
        #st.write(fig)
 
    #with col2:
        #st.write(fig3)
 
    #col3, col4 = st.columns(2)
    #with col3:
        #st.write(fig2)
 
    #with col4:
        #st.write(fig4)
 
    #dfAll_sorted['energy_difference'] = dfAll_sorted['Total_green_energy'] - dfAll_sorted['Some_other_energy_column']

    # Calculate energy difference for each date
    date_energy_differences = []

    # Iterate over unique dates in dfAll
    for date in dfAll['date'].unique():
        stored_location_df = dfAll[(dfAll['city'] == stored_location) & (dfAll['date'] == date)]
        location_df = dfAll[(dfAll['city'] == location) & (dfAll['date'] == date)]
        stored_energy = stored_location_df['Total_green_energy'].sum()
        location_energy = location_df['Total_green_energy'].sum()
        energy_difference = location_energy - stored_energy

        date_energy_differences.append((date, energy_difference))

    # Create a DataFrame from the list of (date, energy_difference) tuples
    df_energy_diff = pd.DataFrame(date_energy_differences, columns=['date', 'energy_difference'])

    # Sort the DataFrame by date
    df_energy_diff = df_energy_diff.sort_values('date')

    # Round the energy_difference column to one decimal place
    df_energy_diff['energy_difference'] = df_energy_diff['energy_difference'].round(2)

    # Plot the energy differences using Plotly Express
    fig = px.bar(df_energy_diff, x='date', y='energy_difference',
                text='energy_difference', color='energy_difference',
                color_continuous_scale=['red', 'orange', 'green'],
                labels={'energy_difference': 'Energy difference (Kwh)'},
                title='Energy difference by Date')

    # Update x-axis tick format to display dates correctly
    fig.update_xaxes(type='category')

    # Center the title
    fig.update_layout(title=dict(text='Energy difference by date', x=0.35))

    # Add buffer to the y-axis range
    buffer = 50  # Adjust the buffer value as needed
    min_value = df_energy_diff['energy_difference'].min() - buffer
    max_value = df_energy_diff['energy_difference'].max() + buffer
    fig.update_layout(yaxis=dict(range=[min_value, max_value]))
    fig.update_layout(width=900)

    # Set text position to 'outside' for better label alignment
    fig.update_traces(textposition='outside')

    # Show the figure using st.plotly_chart
    st.plotly_chart(fig)
 

     # Here I sorted the dataframe on 'total_green_energy' and 'date' too see after in a plot (fig3) what the total amount of generated energy is for every location.
    # In this plot (fig3) you can see easily what location has more generated energy and what location has less.
    # In fig4 you can see for every date the location that has the most energy generated with also the amount showing.
 
    # Sort the DataFrame by 'Total_green_energy' within each 'date' group in descending order
    dfAll_sorted = dfAll.sort_values(by=['date', 'Total_green_energy'], ascending=[True, False])
 
    #col1, col2 = st.columns(2)
    #with col1:
        #st.write(fig2)
 
    #with col2:
        #st.write(fig3)
 
    fig = px.bar(dfAll_sorted, x='date', y='Total_green_energy', color='city', barmode='group')
    fig.update_layout(title="Total amount of green energy for every location", title_x=0.25)
    fig.update_layout(width=900)
    st.write(fig)

    # Create a Plotly bar chart with the sorted DataFrame
    fig2 = px.bar(dfAll_sorted, x='date', y='Es', color='city', barmode='group')
    fig2.update_layout(title="Solar energy for every location", title_x=0.30)
    fig2.update_layout(width=900)
    #fig2.update_layout(showlegend=False)
    st.write(fig2)
 
    fig3 = px.bar(dfAll_sorted, x='date', y='Ew', color='city', barmode='group')
    fig3.update_layout(title="Wind energy for every location", title_x=0.30)
    fig3.update_layout(width=900)
    st.write(fig3)
 

# def weather_forecast(city1_name, city1_latitude, city1_longitude, city2_name, city2_latitude, city2_longitude):
#     def fetch_weather_data(city_name, latitude, longitude): # Function to fetch and process weather data
#         url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=sunshine_duration,wind_speed_10m"
#         response = req.get(url)
#         data = response.json()
#         df = pd.DataFrame(data["hourly"])
#         df["date"] = pd.to_datetime(df["time"]).dt.date
#         df["sunshine_duration"] = round(df["sunshine_duration"] / 3600, 1)
#         df["wind_speed_10m"] = df["wind_speed_10m"].round(1)
#         df = df.drop("time", axis=1)
#         df = df.groupby("date").agg({"sunshine_duration": "sum", "wind_speed_10m": "mean"}).reset_index()
#         return df
 
#     df_city1 = fetch_weather_data(city1_name, city1_latitude, city1_longitude) # Fetch weather data for both cities
#     df_city2 = fetch_weather_data(city2_name, city2_latitude, city2_longitude)
 
#     plt.style.use("dark_background") # Set dark mode style for Matplotlib
 
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5)) # Create a single figure with two subplots (horizontally arranged)
 
#     bar_width = 0.4  # Plot wind speed comparison # Width of each bar
#     index = np.arange(len(df_city1))  # Index for x-axis positioning
 
#     ax1.bar(index - bar_width/2, df_city1["wind_speed_10m"], width=bar_width, color="skyblue", label=f"{city1_name} Wind Speed (m/s)")
#     ax1.bar(index + bar_width/2, df_city2["wind_speed_10m"], width=bar_width, color="orange", label=f"{city2_name} Wind Speed (m/s)")
 
#     for i, val in enumerate(df_city1["wind_speed_10m"]): # Annotate bars with actual values
#         ax1.text(i - bar_width/2, val + 0.1, f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=8)
#     for i, val in enumerate(df_city2["wind_speed_10m"]):
#         ax1.text(i + bar_width/2, val + 0.1, f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=8)
 
#     ax1.set_xlabel("Date", color="white")
#     ax1.set_ylabel("Wind Speed (m/s)", color="white")
#     ax1.set_title("Comparison of Wind Speed between Amsterdam & Madrid", color="white", pad=50)
#     ax1.set_xticks(index)
#     ax1.set_xticklabels(df_city1["date"], rotation=30)
#     ax1.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), facecolor="black")
 
#     ax2.bar(index - bar_width/2, df_city1["sunshine_duration"], width=bar_width, color="skyblue", label=f"{city1_name} Sunshine Duration (hours)") # Plot sunshine duration comparison
#     ax2.bar(index + bar_width/2, df_city2["sunshine_duration"], width=bar_width, color="orange", label=f"{city2_name} Sunshine Duration (hours)")
 
#     for i, val in enumerate(df_city1["sunshine_duration"]): # Annotate bars with actual values
#         ax2.text(i - bar_width/2, val + 0.1, f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=8)
#     for i, val in enumerate(df_city2["sunshine_duration"]):
#         ax2.text(i + bar_width/2, val + 0.1, f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=8)
 
#     ax2.set_xlabel("Date", color="white")
#     ax2.set_ylabel("Sunshine Duration (hours)", color="white")
#     ax2.set_title("Comparison of Sunshine Duration between Amsterdam & Madrid", color="white", pad=50)
#     ax2.set_xticks(index)
#     ax2.set_xticklabels(df_city1["date"], rotation=30)
#     ax2.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), facecolor="black")
 
#     st.pyplot(fig) # Display the plots using Streamlit
 
#     df_merged = pd.merge(df_city1, df_city2, on="date", suffixes=(f" ({city1_name})", f" ({city2_name})")) # Merge both dataframes based on the date
 
#     df_merged[f"wind_speed_difference_Amsterdam"] = (df_merged[f"wind_speed_10m ({city1_name})"] - df_merged[f"wind_speed_10m ({city2_name})"]).apply(lambda x: f"{x:.1f}") # Calculate difference columns
#     df_merged[f"sunshine_duration_difference_Amsterdam"] = (df_merged[f"sunshine_duration ({city1_name})"] - df_merged[f"sunshine_duration ({city2_name})"]).apply(lambda x: f"{x:.1f}")
 
#     df_merged = df_merged[["date", # Rearrange columns for better visualization
#                            f"wind_speed_10m ({city1_name})", f"wind_speed_10m ({city2_name})",
#                            f"wind_speed_difference_Amsterdam",
#                            f"sunshine_duration ({city1_name})", f"sunshine_duration ({city2_name})",
#                            f"sunshine_duration_difference_Amsterdam"]]
 
#     P = 2250 # Define the values of the fixed variables for the energy calculation
#     Cp = 0.6  
#     Cf = 0.3  
#     a = 20  # amount of wind turbines / wind mills
 
#     y = 325
#     q = 0.8
#     n = 100 # amount of solar panels
 
#     v = 1.008
 
#     enegetic_penalty = 10 # The energetic penalty is 1 Kwh for 100 GB
 
#     def calculate_wind_energy(row):  # Function to calculate E(w) based on the provided equation
#         t = row[f"wind_speed_10m ({city1_name})"]  # Get the wind speed value from city1
#         return round(v * a * t, 1) # (P * Cp * Cf * t * a / 1000, 1)
 
#     df_merged['E(w) / Amsterdam'] = df_merged.apply(calculate_wind_energy, axis=1) # Apply the function to create a new column 'E(w)' in the merged DataFrame
 
#     def calculate_wind_energy_2(row): # Function to calculate E(w) based on the provided equation
#         t = row[f"wind_speed_10m ({city2_name})"]  # Get the wind speed value from city1
#         return round(v * a * t, 1) # (P * Cp * Cf * t * a / 1000, 1)
 
#     df_merged['E(w) / Madrid'] = df_merged.apply(calculate_wind_energy_2, axis=1) # Apply the function to create a new column 'E(w)' in the merged DataFrame
 
 
#     def calculate_solar_energy(row): # Function to calculate E(s) based on the provided equation
#         z = row[f"sunshine_duration ({city1_name})"]  # Get the sunshine duration value from city1
#         return round(y * z * q * n / 1000, 1)
 
#     df_merged['E(s) / Amsterdam'] = df_merged.apply(calculate_solar_energy, axis=1) # Apply the function to create a new column 'E(s)' in the merged DataFrame
 
#     def calculate_solar_energy_2(row): # Function to calculate E(s) based on the provided equation
#         z = row[f"sunshine_duration ({city2_name})"]  # Get the sunshine duration value from city1
#         return round(y * z * q * n / 1000, 1)
 
#     df_merged['E(s) / Madrid'] = df_merged.apply(calculate_solar_energy_2, axis=1) # Apply the function to create a new column 'E(s)' in the merged DataFrame
 
#     df_merged['Total green energy Amsterdam'] = df_merged['E(w) / Amsterdam'] + df_merged['E(s) / Amsterdam']
#     df_merged['Total green energy Madrid'] = df_merged['E(w) / Madrid'] + df_merged['E(s) / Madrid']
 
#     df_merged["Difference"] = df_merged["Total green energy Madrid"] - df_merged["Total green energy Amsterdam"] - enegetic_penalty # Calculate difference and label
 
#     def calculate_label(value):
#         if value > 100:
#             return "yes"
#         elif value < -100:
#             return "no"
#         else:
#             return "possibly"
 
#     df_merged["Label"] = df_merged["Difference"].apply(calculate_label)
 
#     # st.write("Merged Weather Data with Energy Calculation:")
#     st.write(df_merged.set_index("date")) # Display the merged dataframe with the calculated energy column
 
 
#     fig3, ax3 = plt.subplots(figsize=(4, 2)) # Set the desired figure size (width, height) in inches
 
#     label_colors = {'yes': 'green', 'no': 'red', 'possibly': 'orange'} # Define custom colors for labels
 
#     colors = [label_colors[label] for label in df_merged['Label'].unique()] # Create color palette using custom colors
 
#     sns.barplot(x='date', y='Difference', hue='Label', data=df_merged, ax=ax3, palette=colors) # Plotting the bar chart with labels
#     sns.set_context("talk")
 
#     df_merged = df_merged.reset_index(drop=True) # Reset index to ensure a valid sequential index starting from 0
 
#     ax3.set_xlabel('Date', fontsize=6)
#     ax3.set_ylabel('Difference', fontsize=6)
#     ax3.set_title('Transfer labels for Amsterdam --> Madrid', fontsize=8)
#     ax3.set_xticklabels(df_merged['date'], rotation=30)  # Rotate x-axis labels for better readability
#     plt.tick_params(axis='x', labelsize=6)  # Font size for x-axis tick labels
#     plt.tick_params(axis='y', labelsize=6)  # Font size for y-axis tick labels
 
#     ax3.legend(title='Label', title_fontsize='6', loc='upper right', fontsize='6') # Customize legend and other settings
 
#     st.pyplot(fig3) # Display the plot using Streamlit