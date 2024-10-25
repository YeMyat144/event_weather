import streamlit as st
import requests
from datetime import datetime

# Set the page configuration
st.set_page_config(page_title="🌤️ Weather App", page_icon="🌤️", layout="centered")

# Add a background image (Optional)
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        background-image: url("https://images.unsplash.com/photo-1495701073176-7faf0e2e8cbb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1650&q=80");
        background-size: cover;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# API key for OpenWeatherMap
API_KEY = "901409775654935ad735712ac7b14df2"

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("City not found or API request failed.")
        return None

# Function to format timestamp into readable format
def format_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Sidebar input for city name
st.sidebar.header("🔍 Search for City Weather")
city_name = st.sidebar.text_input("🌆 City Name", value="New York")

# If the user provides a city name, fetch the weather data
if city_name:
    weather_data = get_weather_data(city_name, API_KEY)
    
    if weather_data:
        st.markdown(f"<h2 style='text-align: center;'>{weather_data['name']}, {weather_data['sys']['country']}</h2>", unsafe_allow_html=True)
        
        # Weather icon
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Display weather icon in the center
        st.markdown(f"<div style='text-align: center;'><img src='{icon_url}'></div>", unsafe_allow_html=True)
        
        # Display temperature and weather description
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        weather_description = weather_data['weather'][0]['description'].capitalize()
        
        st.markdown(f"<h3 style='text-align: center;'>🌡️ {temp} °C | {weather_description}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Feels Like: {feels_like} °C</p>", unsafe_allow_html=True)
        
        # Display additional weather information
        st.write("### Additional Information:")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("💨 Wind Speed", f"{weather_data['wind']['speed']} m/s")
            st.metric("💧 Humidity", f"{weather_data['main']['humidity']} %")
        with col2:
            st.metric("📏 Pressure", f"{weather_data['main']['pressure']} hPa")
            st.metric("🌐 Wind Direction", f"{weather_data['wind']['deg']}°")
        
        # Show sunrise and sunset times
        sunrise = format_time(weather_data['sys']['sunrise'])
        sunset = format_time(weather_data['sys']['sunset'])
        st.write(f"🌅 **Sunrise**: {sunrise} UTC | 🌇 **Sunset**: {sunset} UTC")
        
        # Optionally add more details for rain/snow
        if "rain" in weather_data:
            st.write(f"🌧️ **Rain (last 1h)**: {weather_data['rain']['1h']} mm")
        if "snow" in weather_data:
            st.write(f"❄️ **Snow (last 1h)**: {weather_data['snow']['1h']} mm")
else:
    st.write("Please enter a city name in the sidebar to see the weather information.")

# Add footer with data source
st.markdown(
    """
    <div style='text-align: center;'>
    <br>
    <p>Powered by <a href="https://openweathermap.org/" target="_blank">OpenWeatherMap</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
