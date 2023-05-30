import sys
import os
import threading
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, request, render_template, session,send_file,redirect,url_for,make_response,flash
from flask_login import login_user, logout_user,login_required,current_user
from datetime import datetime 
from main import app ,login#,models
from service import session,user_service
from flask_login import login_user, logout_user,login_required

@app.route('/api_product_detail', methods=['POST'])
def api_product_detail():
    if request.method == 'POST':
        email='1954052067nhat@ou.edu.vn'
        session.check_price(request.form['url'],email,request.form['price'])
        return redirect(url_for('test'))
        return render_template('test2.html')
    
@app.route('/add_url_process', methods=['POST'])
def add_url_process():
    flag, id=session.add_url(request.form['url'],request.form['price'],current_user.id)
    print(id)
    session.check_price(id)
    return redirect(url_for('index'))

@app.route('/register')
def register():
        return render_template('register.html')

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.user_role =='ADMIN':
            crawlers=session.get_url_with_user(current_user.id)
            return render_template('adminPage.html',crawlers=crawlers)
        else:
            crawlers=session.get_url_with_user(current_user.id)
            return render_template('userPage.html',crawlers=crawlers)

@app.route('/register_process', methods=['POST'])
def register_user():
    # Lấy dữ liệu từ request
    data = request.get_json()
    print(data)
    # print(user_service.save_new_user(data))
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

def check():
    while True:
        time=[] 
        for i in time:
            print("Hi")
            

def run_my_function():
    thread = threading.Thread(target=check)
    thread.daemon = True
    thread.start()

@login.user_loader
def get_user(user_id):
    return user_service.get_user_by_id(user_id)

if __name__ == '__main__':
    #run_my_function()
    app.run(host='0.0.0.0', port=80)