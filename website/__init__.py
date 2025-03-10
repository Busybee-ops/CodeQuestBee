from flask import Flask, render_template, request 
from flask_cors import CORS
from website.views import views  # Importing views blueprint
from website.project1.mainp1 import project1  # Importing project1 blueprint
from website.project2.mainp2 import project2  # Importing project2 blueprint
from website.tictactoe.game_main import tictactoe # Importing tictactoe blueprint
from flask import Blueprint
import logging
import os
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom(24)  # Set a secret key for session management
    CORS(app)
    app.register_blueprint(views)
    app.register_blueprint(project1, url_prefix='/project1')
    app.register_blueprint(project2, url_prefix='/project2')
    app.register_blueprint(tictactoe, url_prefix='/tictactoe')
    return app