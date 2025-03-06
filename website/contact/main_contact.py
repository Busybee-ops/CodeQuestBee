from flask import Blueprint, request, jsonify, render_template

contact = Blueprint('contact', __name__, template_folder='templates')

@contact.route('/', methods=['GET', 'POST'])
def handle_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Check if all fields are filled out
        if not name or not email or not message:
            return jsonify({'error': 'All fields are required.'}), 400

        # Simulate a successful submission response
        return f"""
            <div class="container mt-4">
                <h4>Thank you for contacting us, {name}. We will get back to you soon!</h4>
               <a href="#" onclick="loadTab('/contact/', document.querySelector('[data-url=\'/contact/\']'))" class="btn btn-primary mt-3">Again</a>
            </div>
        """

    return render_template('index_contact.html')