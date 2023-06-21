from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config_by_name
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
config_name='prod'
app = Flask(__name__)
app.config.from_object(config_by_name[config_name])
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'my_login'
ZONE="Asia/Bangkok"
CONFIG=config_by_name[config_name]

 