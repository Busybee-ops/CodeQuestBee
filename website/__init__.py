from flask import Flask, render_template, request 
from flask_cors import CORS
from website.views import views  # Importing views blueprint
from website.project1.mainp1 import project1  # Importing project1 blueprint
from website.project2.mainp2 import project2  # Importing project2 blueprint
from website.contact.main_contact import contact  # Importing contact blueprint
from flask import Blueprint
import logging
import os

def configure_cors(app):
    CORS(app, resources={
        r"/project1/*": {"origins": "*"},
        r"/project2/*": {"origins": "*"},
        r"/contact/*": {"origins": "*"}
    })

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

    configure_cors(app)

    # Register the blueprints for Project 1 and Project 2
    app.register_blueprint(project1, url_prefix='/project1')  # All routes under '/project1' will use the project1 blueprint
    app.register_blueprint(project2, url_prefix='/project2')  # All routes under '/project2' will use the project2 blueprint
    app.register_blueprint(contact, url_prefix='/contact')
    app.register_blueprint(views)  # Register the views blueprint

    return app