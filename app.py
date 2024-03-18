import streamlit as st
import pandas as pd
import requests as req

st.write('Here should come some green labelling...')

# 53.333950289758135, 6.920911731760793
url = "https://api.open-meteo.com/v1/forecast?latitude=53.33&longitude=6.9181&daily=temperature_2m_max"
# read the data from url
response = req.get(url)
data = response.json()
# convert the data to a pandas dataframe
df = pd.DataFrame(data['daily']['temperature_2m_max'])
# print the dataframe
st.write(df)