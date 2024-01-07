import logging
import multiprocessing
import sys
import os
import threading
import time
import traceback

import requests
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import  Flask, jsonify,abort, request, render_template, session,send_file,redirect,url_for,make_response,flash,Response
from flask_login import login_user, logout_user,login_required,current_user
from datetime import datetime 
from main import app ,login,logger#,models
from flask_sqlalchemy import SQLAlchemy
from service import session,user_service,schedule
from service.logger import config_log
from flask_login import login_user, logout_user,login_required
from model import models
is_check_price_running = False
is_flask_running = False



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception
    logger.error(traceback.format_exc())
    return render_template('error.html'),500

@app.route('/delete_url/<string:id>', methods=['POST'])
@login_required
def delete_url(id):
    session.delet_url_with_id(id)
    return redirect(url_for('all_url'))


@app.route('/delete_user/<string:id>', methods=['POST'])
@login_required
def delete_user(id):
    user_service.delet_user_with_id(id)
    return redirect(url_for('index'))
    
@app.route('/change_password_user/<string:id>', methods=['POST'])
@login_required
def change_password_user(id):
    user_service.change_password_user(id,request.form['password'])
    return redirect(url_for('index'))

@app.route('/add_url_process', methods=['POST'])
@login_required
def add_url_process():
    try:
        option=request.form['option']
    except Exception:
        option=None
    count_urls=session.count_url()
    if count_urls > 150:
        return redirect(url_for('index', response_status_code=301))
    else:
        flag, id=session.add_url(request.form['url'],request.form['price'],current_user.id,option,request.form['name_product'])
        return redirect(url_for('index'))

@app.route('/register')
def register():
    if current_user.user_type.user_role =='ADMIN':
        return render_template('signUp.html')
    else:
        abort(404)

@app.route('/all_url')
@login_required
def all_url():
    if current_user.user_type.user_role =='ADMIN':
        crawlers=session.get_all_url()
        return render_template('UrlManagement.html',crawlers=crawlers)
    else:
        abort(404)
    

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        response_status_code = request.args.get('response_status_code')
        if current_user.user_type.user_role =='ADMIN':    
            users=session.get_all_users()
            return render_template('userMangementPage.html',users=users)
        else:
            crawlers=session.get_url_with_user(current_user.id)
            mess= None
            if response_status_code == str(301):
                mess="Maximum URL"
            return render_template('userPage.html',crawlers=crawlers,current_user=current_user,mess=mess)
    else:
        return redirect("/login")

@app.route('/register_process', methods=['POST'])
@login_required
def register_user():
    data = request.get_json()
    return user_service.save_new_user(data)

@app.route('/login')
def my_login():
    return render_template('loginForm.html')

@app.route("/login", methods=['POST'])
def my_login_process():
    email = request.form['email']
    password = request.form['password']
    u = user_service.auth_user(email, password)
    if u:
        login_user(user=u)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else '/')

    return render_template('loginForm.html')


@app.route("/logout")
@login_required
def my_logout():
    logout_user()
    return redirect("/login")

@app.before_first_request
def run_my_function():
    global is_check_price_running, is_flask_running
    if is_check_price_running == False:
        is_check_price_running = True
        thread = threading.Thread(target=schedule.schedule_check_price)
        thread.daemon = True
        thread.start()
        

# def set_up_log():
#     handler = logging.StreamHandler()
#     file_handler.setLevel(logging.DEBUG)
#     handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(Formatter(
#         '%(asctime)s %(levelname)s: %(message)s '
#         '[in %(pathname)s:%(lineno)d]'
#      ))
#      handler.setFormatter(Formatter(
#         '%(asctime)s %(levelname)s: %(message)s '
#         '[in %(pathname)s:%(lineno)d]'
#      ))
#      app.logger.addHandler(handler)
#      app.logger.addHandler(file_handler)
  
def start_app():
    global is_flask_running
    is_flask_running = True
    
    app.run(host='0.0.0.0', port=1011,threaded=True)

@login.user_loader
def get_user(user_id):
    return user_service.get_user_by_id(user_id)

if __name__ == '__main__':
    start_app()
   