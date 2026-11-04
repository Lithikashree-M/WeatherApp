
import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_KEY")
print("API key loaded:", bool(API_KEY))

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Function to get current weather
def get_weather(city):

    if not API_KEY:
        print("API key not found. Check your .env file.")
        return None

    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            CURRENT_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            print("City not found. Please try again.")
            return None

        if response.status_code == 401:
            print("Invalid API key or key not activated yet.")
            return None

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:
        print("Network error. Check your internet connection.")
        return None

# Function to get five-day forecast
def get_forecast(city):

    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            print("Invalid or inactive API key.")
            return None

        response.raise_for_status()

        data = response.json()

        daily_forecast = {}

        for item in data.get("list", []):

            date = item["dt_txt"].split(" ")[0]

            if date not in daily_forecast:
                daily_forecast[date] = item

        return daily_forecast

    except requests.exceptions.RequestException:
        print("Unable to fetch forecast.")
        return None

# Function to display weather
def display_weather(data):

    if not data:
        return

    print("\n" + "=" * 40)
    print("       CURRENT WEATHER REPORT")
    print("=" * 40)

    print("City:", data.get("name", "Unknown"))
    print("Temperature:", data.get("main", {}).get("temp", "N/A"), "°C")
    print("Humidity:", data.get("main", {}).get("humidity", "N/A"), "%")

    weather = data.get("weather", [{}])[0]

    print("Description:", weather.get("description", "N/A"))

    wind = data.get("wind", {})

    print("Wind Speed:", wind.get("speed", "N/A"), "m/s")

    print("=" * 40)

# Function to display forecast
def display_forecast(forecast):

    if not forecast:
        return

    print("\n       FIVE-DAY WEATHER FORECAST")
    print("-" * 65)

    print(f"{'Date':<15}{'Temperature':<20}{'Description'}")
    print("-" * 65)

    for date, item in list(forecast.items())[:5]:

        temp = item.get("main", {}).get("temp", "N/A")

        description = item.get("weather", [{}])[0].get(
            "description", "N/A"
        )

        print(f"{date:<15}{str(temp) + ' °C':<20}{description}")

    print("-" * 65)

# Main program
print("\nWELCOME TO PYTHON WEATHER APP")

while True:

    city = input("\nEnter city name (press Enter to exit): ").strip()

    if not city:
        print("Thank you for using Weather App!")
        break

    weather_data = get_weather(city)

    if weather_data:

        display_weather(weather_data)

        forecast_data = get_forecast(city)

        display_forecast(forecast_data)