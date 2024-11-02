import streamlit as st
import requests
from datetime import datetime, time
import pandas as pd
import random

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

# App Title and Sidebar
st.set_page_config(page_title="WeatherWise", page_icon="🌦️")
st.title("WeatherWise 🌦️")
st.write("Create events with weather insights and track RSVPs in real-time.")

# Sidebar inputs for Event Creation
st.sidebar.header("🗓️ Create an event")
event_name = st.sidebar.text_input("Event Name", placeholder="e.g., Birthday Party")
event_date = st.sidebar.date_input("Event Date", datetime.now().date())
event_time = st.sidebar.time_input("Event Time", time(12, 0))  # Set default time to 12:00 PM
location = st.sidebar.text_input("Location (City name)", placeholder="e.g., New York")
units = st.sidebar.radio("Units", ["metric", "imperial"])
lang = st.sidebar.selectbox("Language", ["en", "es", "fr", "de"])

# Sample names for initial RSVP list
sample_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey"]

# Initialize RSVP list with sample names if not already set
if 'rsvp_list' not in st.session_state:
    st.session_state['rsvp_list'] = random.sample(sample_names, 3)  # Pick 3 random names

if st.sidebar.button("Create"):
    if location:
        # Geocoding API to fetch latitude and longitude
        geocode_response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={API_KEY}"
        )
        
        if geocode_response.status_code == 200 and geocode_response.json():
            geocode_data = geocode_response.json()[0]
            lat, lon = geocode_data["lat"], geocode_data["lon"]
            
            weather_data = get_weather(lat, lon, units, lang)
            if weather_data:
                temp = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                icon = weather_data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                
                # Event display in a table
                event_data = {
                    "Detail": ["Event Name", "Date", "Time", "Location", "Temperature", "Condition"],
                    "Information": [
                        event_name,
                        event_date.strftime('%B %d, %Y'),
                        event_time.strftime('%I:%M %p'),
                        location,
                        f"{temp}° ({units.capitalize()})",
                        description.capitalize()
                    ]
                }
                event_df = pd.DataFrame(event_data)
                st.table(event_df)
                st.image(icon_url, width=100)
                
                # Countdown Timer
                event_datetime = datetime.combine(event_date, event_time)
                time_remaining = event_datetime - datetime.now()
                days_remaining = time_remaining.days
                hours_remaining, remainder = divmod(time_remaining.seconds, 3600)
                minutes_remaining = remainder // 60
                
                st.write(f"**Countdown:** {days_remaining} days, {hours_remaining} hours, {minutes_remaining} minutes")
                
                # RSVP section
                st.subheader("RSVP to Event")
                
                guest_name = st.text_input("Your Name", key="guest_name")
                if st.button("RSVP"):
                    if guest_name:
                        st.session_state['rsvp_list'].append(guest_name)
                        st.success(f"RSVP confirmed for {guest_name}!")
                        st.experimental_rerun() 
                    else:
                        st.error("Please enter your name.")
                
                # Display RSVP List with delete functionality
                if st.session_state['rsvp_list']:
                    st.write("### RSVP List")
                    for i, guest in enumerate(st.session_state['rsvp_list']):
                        col1, col2 = st.columns([3, 1])
                        col1.write(guest)
                        if col2.button("Delete", key=f"delete_{i}"):
                            st.session_state['rsvp_list'].pop(i)
                            st.success(f"{guest} has been removed from the RSVP list.")
                            st.experimental_rerun()
                    
            else:
                st.error("Weather data could not be retrieved.")
        else:
            st.error("Invalid location.")
    else:
        st.error("Please enter a location.")
