import uuid
import datetime
import sys
import os
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import db,login
from model.models import User


import hashlib
import sys
import os

def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(email, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.email.__eq__(email),
                             User.password.__eq__(password)).first()
    

   

def save_new_user(data):
    try:
        if 'user_name' not in data or 'email' not in data or 'password' not in data:
            response_object = {
                'status': 'fail',
                'message': 'Missing required fields'
            }
            return response_object, 400
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            if data['password'].__eq__(data['password_confirm']):          
                password = str(hashlib.md5(data['password'].encode('utf-8')).hexdigest())
                new_user = User( id=str(uuid.uuid4()), user_name=data['user_name'], password=password,email=data['email'])
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
        print(e)
        return response_object, 409



def get_all_users():
    return User.query.all()




