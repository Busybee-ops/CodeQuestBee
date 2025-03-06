import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from website.project1.mainp1 import project1 as project1_module
from website.project2.mainp2 import project2 as project2_module
from website.contact.main_contact import contact as contact_module
from flask import Blueprint

views = Blueprint('views', __name__)

# Define the main landing page route
@views.route('/', methods=['GET', 'POST'])
def base():
    session['visited_landing'] = True  # Set session variable when landing page is visited
    session['last_tab'] = 'home'  # Default to home tab
    return render_template('home.html')

@views.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('visited_landing') or session.get('last_tab') != 'home':
        return redirect(url_for('views.base'))  # Redirect to landing page if accessed directly
    session['last_tab'] = 'home'
    return render_template('home.html')

# Define the route for the contact page
@views.route('/contact')
def contact():
    if not session.get('visited_landing') or session.get('last_tab') != 'contact':
        return redirect(url_for('views.base'))  # Redirect to landing page if accessed directly
    session['last_tab'] = 'contact'
    return render_template('contact.html')

# Define the route for the project1 page
@views.route('/project1')
def project1():
    if not session.get('visited_landing') or session.get('last_tab') != 'project1':
        return redirect(url_for('views.base'))  # Redirect to landing page if accessed directly
    session['last_tab'] = 'project1'
    return render_template('project1.html')

# Define the route for the project2 page
@views.route('/project2')
def project2():
    if not session.get('visited_landing') or session.get('last_tab') != 'project2':
        return redirect(url_for('views.base'))  # Redirect to landing page if accessed directly
    session['last_tab'] = 'project2'
    return render_template('project2.html')

@views.route('/update_last_tab', methods=['POST'])
def update_last_tab():
    data = request.get_json()
    session['last_tab'] = data['last_tab']
    return '', 204
