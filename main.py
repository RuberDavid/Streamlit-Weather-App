import streamlit as st
import modules.weather as we

st.title("Current and last month weather")

MAX_LONGITUDE = 180
MIN_LONGITUDE = -180
MAX_LATITUDE = 90
MIN_LATITUDE = -90

first_name = st.text_input("first_name", max_chars=35)
last_name = st.text_input("last_name", max_chars=35)
email = st.text_input("email", max_chars=254)

col1, col2, col3 = st.columns(3)

with col1:
    # TODO: function to read  and validate location parameters
    latitude = st.number_input("latitude", max_value=MAX_LATITUDE, min_value=MIN_LATITUDE)
with col2:
    longitude = st.number_input("longitude", max_value=MAX_LONGITUDE, min_value=MIN_LONGITUDE)
with col3:
    location_by_name = st.text_input("Location name")
# look for weather data

location = {"latitude": latitude, "longitude": longitude}
st.text(location)

# button to search weather
st.text(we.current_weather(location))

# store data


st.subheader('Records')
