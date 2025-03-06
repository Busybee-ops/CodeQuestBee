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
                weather_info = f"Weather in {location}: {weather_data['weather'][0]['description']}, " \
                               f"Temperature: {weather_data['main']['temp']}K"
                return f"""
                    <h4>{weather_info}</h4>
                    <a href="#" onclick="loadTab('/project2/', document.querySelector('[data-url=\'/project2/\']'))" class="btn btn-primary mt-3">Get Weather Again</a>
                """  # Return weather data as HTML snippet
            else:
                error_message = "Weather data not found. Please check your inputs."
                return f"""
                    <p class="text-danger">{error_message}</p>
                    <a href="#" onclick="loadTab('/project2/', document.querySelector('[data-url=\'/project2/\']'))" class="btn btn-primary mt-3">Try Again</a>
                """  # Return error message as HTML snippet
        except Exception as e:
            return f"""
                <p class="text-danger">Error retrieving weather data. Please try again.</p>
              <a href="#" onclick="loadTab('/project2/', document.querySelector('[data-url=\'/project2/\']'))" class="btn btn-primary mt-3">Weather Again</a>
            """  # Return error message as HTML snippet

    # If the method is GET, just render the weather form
    return render_template('indexp2.html')
