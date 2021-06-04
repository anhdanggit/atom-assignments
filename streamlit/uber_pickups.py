
# Refrences: https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Fetch Data
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# UI
st.title('Uber pickups in NYC') # Title of the App

data_load_state = st.text('Loading data...') ## -> Create a text element to inform reader that the data is loading
data = load_data(1000) ## -> To make it light for render
data_load_state.text('DONE! (using st.cache)') ## -> Update the text that the result is ready

## Expect Raw Data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

## Histogram: pickups by hour of day
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] ## -> np to breaks down bins of pickup time
#st.write(hist_values) ## -> print to test
st.bar_chart(hist_values)

## Plot data on a map
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader('Mapp of all pickups')
st.map(filtered_data)


# Run: streamlit run streamlit/uber_pickups.py