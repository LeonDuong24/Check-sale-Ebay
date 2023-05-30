from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config_by_name


config_name='dev'
app = Flask(__name__)
app.config.from_object(config_by_name[config_name])
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'my_login'

