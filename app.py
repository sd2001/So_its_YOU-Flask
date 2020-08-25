from flask import Flask, render_template, redirect, url_for, flash, session, request
import pymongo
from pymongo import MongoClient
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
import bcrypt
from flask_login import login_user,current_user

client=MongoClient('mongodb+srv://swarnabha:swarnabhadb@cluster0.yfmwo.mongodb.net/Logbase?retryWrites=true&w=majority')
db=client['Users']


app=Flask(__name__)
name=""

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')
    


@app.route('/login',methods=['POST'])
def login_post():
    email=request.form.get('email')
    password=request.form.get('pass')
    data=db.credentials
    flag=False
    
    for i in data.find():
        if i['email']==email:
            name=i['username']
            flag=True
            if check_password_hash(i['password'], password):                               
                return redirect(url_for('profile'))
            
              
             
    if email is None and password is None:
        flash("Please fill both the fields and Try Again")
        return redirect(url_for('login'))
    
    if flag==False:
        flash("Invalid Credentials")
        return redirect(url_for('login'))
    
    return redirect(url_for('login'))
   

    

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def reg_post():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('pass')
    password=generate_password_hash(password, method='sha256')
    
    
    data=db.credentials
    for i in data.find():
        if i['email']==email:  
            flash("Your Email Address is already registered with us")
            return redirect(url_for('login')) 
    else:   
        user_info={'username': name,
                'email': email,
                'password': password} 
        data.insert_one(user_info)
        session['username']=name
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    #flash("You are kindly requested to Login first")
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__=='__main__':
    app.secret_key = 'hellouserapi'
    app.run(debug=True)
    