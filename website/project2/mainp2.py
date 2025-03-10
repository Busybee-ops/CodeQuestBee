from flask import render_template, request, jsonify
from flask import Blueprint
import requests

project2 = Blueprint('project2', __name__, template_folder='templates')

@project2.route('/', methods=['GET', 'POST'])
def weather_form():
    if request.method == 'POST':
        location = request.form['location']

        # Weather API URL (replace with actual API endpoint and key)
       
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&limit=1&appid=42610234843dc82174cf3eb7ba7f02ce&units=imperial'

        try:
            response = requests.get(api_url)
            weather_data = response.json()

            if weather_data.get("cod") == 200:
                weather_info = {
                    'weather': weather_data['weather'][0]['description'],
                    'temperature': weather_data['main']['temp']
                }
                return jsonify(weather_info)
            else:
                error_message = "Weather data not found. Please check your inputs."
                return jsonify({'error': error_message}), 404
        except Exception as e:
            return jsonify({'error': 'Error retrieving weather data. Please try again.'}), 500

    # If the method is GET, just render the weather form
    return render_template('project2.html')
