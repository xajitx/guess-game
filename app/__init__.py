from flask import Flask

app = Flask(__name__)
from app import admin_views
from app import game_interface
from app import new_Data