import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
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

# Define the route for the game_ttt page
@views.route('/game_ttt')
def game_ttt():
    if not session.get('visited_landing') or session.get('last_tab') != 'game_ttt':
        return redirect(url_for('views.base'))
    session['last_tab'] = 'game_ttt'
    return render_template('game_ttt.html')

@views.route('/update_last_tab', methods=['POST'])
def update_last_tab():
    data = request.get_json()
    session['last_tab'] = data['last_tab']
    return '', 204
