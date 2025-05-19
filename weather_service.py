import zmq
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"

def is_within_14_days(date_str, date_format="%Y-%m-%d"):
    try:
        input_date = datetime.strptime(date_str, date_format).date()
        today = datetime.today().date()
        return input_date <= today + timedelta(days=14)
    except ValueError:
        return False
    

def will_it_rain(city, date, threshold=50):
    params = {
        "q": city,
        "key": API_KEY,
        "dt": date,
        "forecastday": "day"
    }
    # Check if future date is within 14 days
    if not is_within_14_days(date):
        raise ValueError("Forecast not available for more than 14 days ahead")

    # Check if city name is valid
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        errorMsg = data.get("error", {}).get("message", "Something went wrong")
        raise ValueError(f"API Error: {errorMsg}")
    
    forecast = data.get("forecast", {}).get("forecastday", [])
    if not forecast:
        raise ValueError("No forecast data found for the given date")

    chance_of_rain = forecast[0]["day"]["daily_chance_of_rain"]
    return True if chance_of_rain >= threshold else False


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Weather microservice listening...")

while True:
    message = socket.recv_json()
    city = message["city"]
    threshold = message.get("threshold", None)
    date = message["date"]
    try:
        result = will_it_rain(city, date, threshold) if threshold else will_it_rain(city, date)
        socket.send_json({"will_rain": result})
    except Exception as e:
        socket.send_json({"error": str(e)})
