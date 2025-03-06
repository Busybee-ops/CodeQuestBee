from flask import Blueprint, render_template, request

project1 = Blueprint('project1', __name__, template_folder='templates')

@project1.route('/', methods=['GET', 'POST'])
def water_intake():
    if request.method == 'POST':
        weight = float(request.form.get('weight', 0))
        activity_level = request.form.get('activity_level')
        temperature_fahrenheit = float(request.form.get('temperature', 0))

        # Base water intake calculation (1 oz per pound of weight)
        recommended_intake_oz = weight * 1  # 1 oz of water per lb of body weight

        # Convert oz to liters (1 liter = 33.814 oz)
        recommended_intake_liters = recommended_intake_oz / 33.814

        # Adjust for activity level
        activity_adjustment = {
            "sedentary": 0,
            "light": 0.5,      # Additional 0.5L
            "moderate": 1,     # Additional 1L
            "active": 1.5      # Additional 1.5L
        }
        recommended_intake_liters += activity_adjustment.get(activity_level, 0)

        # Adjust for temperature in Fahrenheit
        if temperature_fahrenheit > 86:  # 86°F = 30°C
            # Increase intake by 0.5L for every 5°F above 86°F
            additional_intake = ((temperature_fahrenheit - 86) / 5) * 0.5  # 0.5L for each 5°F above 86°F
            recommended_intake_liters += additional_intake

        # Convert the final recommended intake back to ounces
        recommended_intake_oz_final = recommended_intake_liters * 33.814

        # Return both recommended intake in liters and ounces

        return f"""
             <h4>Recommended Water Intake: {recommended_intake_liters:.2f} Liters or {recommended_intake_oz_final:.2f} Ounces</h4>
             <a href="#" onclick="resetForm()" class="btn btn-primary mt-3">Calculate Again</a>
        """

    return render_template('project1.html')  # Make sure this is your correct template file
