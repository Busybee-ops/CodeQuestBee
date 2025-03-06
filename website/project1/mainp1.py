from flask import Blueprint, render_template, request

project1 = Blueprint('project1', __name__, template_folder='templates')

@project1.route('/', methods=['GET', 'POST'])
def water_intake():
    if request.method == 'POST':
        weight = float(request.form.get('weight', 0))
        activity_level = request.form.get('activity_level')
        temperature = float(request.form.get('temperature', 0))

        # Base water intake calculation (33ml per kg of weight)
        recommended_intake = weight * 0.033  

        # Adjust for activity level
        activity_adjustment = {
            "sedentary": 0,
            "light": 0.5,
            "moderate": 1,
            "active": 1.5
        }
        recommended_intake += activity_adjustment.get(activity_level, 0)

        # Adjust for temperature (if above 30°C, increase intake)
        if temperature > 30:
            recommended_intake += 0.5  # Additional 0.5L for hot weather

        return f"""
            <h4>Recommended Water Intake: {recommended_intake:.2f} liters/day</h4>
            <a href="#" onclick="loadTab('/project1/', document.querySelector('[data-url=\'/project1/\']'))" class="btn btn-primary mt-3">Calculate Again</a>
        """

    return render_template('indexp1.html')  # Make sure this is your correct template file
