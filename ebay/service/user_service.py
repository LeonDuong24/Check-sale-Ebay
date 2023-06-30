import traceback
import uuid
import datetime
import sys
import os
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import db,login
from model.models import User,User_type
from model import models
from service import mysql
import hashlib
import sys
import os
from sqlalchemy import MetaData, Table, create_engine,text
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import CONFIG,ZONE,logger
def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_all_users():
    return models.User.query.all()

def get_url_with_user(user_id):
    return models.CrawlData.query.filter(models.CrawlData.user_id.__eq__(user_id)).all()

def auth_user(email, password):
    try:
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        return User.query.filter(User.email.__eq__(email),
                                User.password.__eq__(password)).first()
    except Exception as e:
        response_object = {
                'status': 'fail',
                'message': 'System error',
            }

def delet_user_with_id(id):
    try:
        engine = create_engine(CONFIG.SQL_URL)
        query_crawl = f"""DELETE  
                        from Crawl_data
                        where user_id= "{id}"
                            """
        flag=mysql.excute_query(query_crawl,engine)
        query = f"""DELETE  
                    from User
                    where id= "{id}"
                        """
        flag=mysql.excute_query(query,engine)
        return True
    except:
        logger.error(traceback.format_exc())
        return False 
    
def change_password_user(id,password):
    try:
        password_encryp = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        engine = create_engine(CONFIG.SQL_URL)
        query = f"""UPDATE User SET password ='{password_encryp}' 
                    where id= "{id}"
                        """
        flag=mysql.excute_query(query,engine)
        return True
    except:
        logger.error(traceback.format_exc())
        return False 

def save_new_user(data):
    try:
        print(str(uuid.uuid4()))
        if 'user_name' not in data or 'email' not in data or 'password' not in data:
            response_object = {
                'status': 'fail',
                'message': 'Missing required fields'
            }
            return response_object, 400
        user = User.query.filter_by(email=data['email']).first()
        user_type = User_type.query.filter_by(user_role='USER').first()
        if not user:
            if data['password'].__eq__(data['password_confirm']):          
                password = str(hashlib.md5(data['password'].encode('utf-8')).hexdigest())
                new_user = User( id=str(uuid.uuid4()), user_name=data['user_name'], password=password,email=data['email'],user_type_id=user_type.id)
                db.session.add(new_user)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Confirmation password is not correct'
                }
                return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists',
            }
            return response_object, 409
    except Exception as e:
        response_object = {
                'status': 'fail',
                'message': 'System error',
            }
        logger.error(traceback.format_exc())
        return response_object, 409





