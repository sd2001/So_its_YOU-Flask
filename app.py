from flask import Flask, render_template, redirect, url_for, flash, session, request
import pymongo
from pymongo import MongoClient
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import bcrypt


client=MongoClient('mongodb+srv://swarnabha:swarnabhadb@cluster0.yfmwo.mongodb.net/Logbase?retryWrites=true&w=majority')
db=client['Users']


app=Flask(__name__)

# login_manager=LoginManager()
# login_manager.login_view='login'



@app.route('/')
def login():
    return render_template('login.html')


# @app.route('/',methods=['POST'])
# def login_post():

    

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def reg_post():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('pass')
    password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    
    data=db.credentials
    existing=data.find_one({'name': name})
    if existing is not None :
        flash("Your Email Address is registered with us, try Logging in")
        return redirect(url_for('reg'))
    else:   
        user_info={'username': name,
                'email': email,
                'password': password} 
        data.insert_one(user_info)
        session['username']=name
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(url_for(login))

if __name__=='__main__':
    app.secret_key = 'hellodoggy'
    app.run(debug=True)
    