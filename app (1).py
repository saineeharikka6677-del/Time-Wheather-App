from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('clock.html')

# --- Timezone endpoint ---
@app.route('/get_time')
def get_time():
    tz_name = request.args.get('tz', 'UTC')
    try:
        timezone = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        timezone = pytz.timezone('UTC')

    now = datetime.now(timezone)
    time_data = {
        'time': now.strftime("%H:%M:%S"),
        'date': now.strftime("%A, %B %d, %Y")
    }
    return jsonify(time_data)

# --- Weather endpoint using wttr.in (no API key needed) ---
@app.route('/get_weather')
def get_weather():
    city = request.args.get('city', 'London')
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        data = response.json()

        weather_info = {
            "temp": data['current_condition'][0]['temp_C'],
            "desc": data['current_condition'][0]['weatherDesc'][0]['value'],
            "city": city.title()
        }
    except Exception:
        weather_info = {"error": "Could not fetch weather data."}
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)
