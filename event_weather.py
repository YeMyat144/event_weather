import streamlit as st
import requests
from datetime import datetime

# Constants
API_KEY = "901409775654935ad735712ac7b14df2"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Helper function to fetch weather
def get_weather(lat, lon, units="metric", lang="en"):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": units,
        "lang": lang
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# User Input for Event
st.title("Weather-Based Event Planner")

st.sidebar.header("Event Creation")
event_name = st.sidebar.text_input("Event Name")
event_date = st.sidebar.date_input("Event Date")
event_time = st.sidebar.time_input("Event Time")
location = st.sidebar.text_input("Location (City name)")
units = st.sidebar.radio("Units", ["metric", "imperial"])
lang = st.sidebar.selectbox("Language", ["en", "es", "fr", "de"])

if st.sidebar.button("Create Event"):
    if location:
        geocode_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={API_KEY}")
        if geocode_response.status_code == 200 and geocode_response.json():
            geocode_data = geocode_response.json()[0]
            lat, lon = geocode_data["lat"], geocode_data["lon"]
            
            weather_data = get_weather(lat, lon, units, lang)
            if weather_data:
                temp = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                
                st.write(f"### {event_name}")
                st.write(f"**Date:** {event_date}")
                st.write(f"**Time:** {event_time}")
                st.write(f"**Location:** {location}")
                st.write(f"**Temperature:** {temp}°")
                st.write(f"**Condition:** {description.capitalize()}")
            else:
                st.error("Weather data could not be retrieved.")
        else:
            st.error("Invalid location.")
    else:
        st.error("Please enter a location.")
