from flask import Blueprint, render_template, request
import joblib
import numpy as np
import pandas as pd
import math
from flask import jsonify
import os

project1 = Blueprint('project1', __name__, template_folder='templates')


# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the model file
model_path = os.path.join(current_dir, 'water_intake_model.pkl')

# Load the model
model = joblib.load(model_path)


@project1.route('/', methods=['GET', 'POST'])
def water_intake():
    if request.method == 'POST':
        weight = float(request.form.get('weight', 0))
        activity_level = request.form.get('activity_level')
        temperature_fahrenheit = float(request.form.get('temperature', 0))
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender')

        # Prepare the input data for the model
        input_data = pd.DataFrame([[weight, activity_level, temperature_fahrenheit, age, gender]], 
                                  columns=['weight', 'activity_level', 'temperature', 'age', 'gender'])
        input_data = pd.get_dummies(input_data, columns=['activity_level', 'gender'], drop_first=True)

        # Ensure all expected columns are present
        for col in model.feature_names_in_:
            if col not in input_data.columns:
                input_data[col] = 0

        # Predict the recommended intake using the model
        model_recommended_intake_liters = model.predict(input_data)[0]

        # Manual calculation for recommended intake
        # Base water intake calculation (0.5 oz per pound of weight)
        base_intake_oz = weight * 0.5

        # Convert oz to liters (1 liter = 33.814 oz)
        base_intake_liters = base_intake_oz / 33.814

        # Adjust for activity level
        activity_adjustment = {
            "sedentary": 0,
            "light": 0.5,      # Additional 0.5L
            "moderate": 1,     # Additional 1L
            "active": 1.5      # Additional 1.5L
        }
        manual_adjusted_intake_liters = base_intake_liters + activity_adjustment.get(activity_level, 0)

        # Adjust for temperature in Fahrenheit
        if temperature_fahrenheit > 70:
            # Increase intake by 0.5L for every 10°F above 70°F
            additional_intake = ((temperature_fahrenheit - 70) / 10) * 0.5
            manual_adjusted_intake_liters += additional_intake

        # Combine the model's prediction with the manual calculation by taking the average
        #final_recommended_intake_liters = (model_recommended_intake_liters + manual_adjusted_intake_liters) / 2

        # Convert the final recommended intake to fluid ounces
        recommended_intake_oz_final =  manual_adjusted_intake_liters * 33.814

        # Calculate the number of bottles needed, rounding up to the nearest whole number
        bottles = math.ceil(recommended_intake_oz_final / 16.9)

        # Return both recommended intake in liters and ounces
        # Return the result as JSON
        return jsonify({
            'liters': manual_adjusted_intake_liters,
            'ounces': recommended_intake_oz_final,
            'bottles': bottles
        })

    return render_template('project1.html')  # Make sure this is your correct template file