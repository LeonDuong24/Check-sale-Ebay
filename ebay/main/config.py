import json
import os
from urllib.parse import quote
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

def get_config_with_env(env):
    root_folder = os.getcwd()
    path_config=os.path.join(root_folder,'config',env+'.json')
    with open(path_config, encoding="utf-8-sig") as f:
                return json.loads( f.read())

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    config=get_config_with_env('dev')
    name_db="WebSale"
    SQLALCHEMY_DATABASE_URI =  f"mysql+pymysql://{config['mysql']['user']}:{config['mysql']['pwd']}@{config['mysql']['host']}/WebSale?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_URL=f"mysql://{config['mysql']['user']}:{config['mysql']['pwd']}@{config['mysql']['host']}:{config['mysql']['port']}/WebSale"



class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = True
    config=get_config_with_env('prod')
    name_db="WebSale"
    SQLALCHEMY_DATABASE_URI =  f"mysql+pymysql://{config['mysql']['user']}:{config['mysql']['pwd']}@{config['mysql']['host']}/WebSale?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_URL=f"mysql://{config['mysql']['user']}:{config['mysql']['pwd']}@{config['mysql']['host']}:{config['mysql']['port']}/WebSale"


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
