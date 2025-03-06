import os 
from flask import Flask, render_template, request
from flask_cors import CORS
from website.project1.mainp1 import project1 as project1_module
from website.project2.mainp2 import project2 as project2_module
from website.contact.main_contact import contact as contact_module
from flask import Blueprint

views = Blueprint('views', __name__)

# Define the main landing page route
@views.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')            

@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Define the route for the contact page
@views.route('/contact')
def contact_view():
    return render_template('contact.html')

# Define the route for the project1 page
@views.route('/project1')
def project1_view():
    return render_template('project1.html')

# Define the route for the project2 page
@views.route('/project2')
def project2_view():
    return render_template('project2.html')