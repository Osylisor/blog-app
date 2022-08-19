from flask import Blueprint, render_template, request, flash, redirect, url_for
from App import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

auth = Blueprint('auth', __name__)



@auth.route('/login', methods = ['GET', 'POST'])
def login():

    if(request.method == 'POST'):
        
     
        #Get the form data
        email = request.form.get('email')
        password = request.form.get('password')

        #Check if the user exists

        user = User.query.filter_by(email = email).first()

        if(user):
            
            if(check_password_hash(user.password, password)):
                flash(f'Login successful, welcome { user.user_name }', category='success')
                login_user(user)
                return redirect(url_for('views.home')) 
            else:
                flash('Incorrect password, please enter the correct password', category='error')

        else:

            flash('This email does not exist, please enter a correct password', category='error')
          
        
    return render_template('login.html')


@auth.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():

    if(request.method == 'POST'):

        #Get data from the form 
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_comfirm = request.form.get('password-comfirm')

        #Validatons for user data

        user = User.query.filter_by(email = email).first()

        if(user):
            flash('This email already exists, try another email', category= 'error')

        elif(len(username) < 3):
            flash('The user name should be at least 3 characters long', category='error')
        
        elif(len(password) < 6):
            flash('The password should be at least 6 characters long', category='error')   
        elif(password != password_comfirm):
            flash('The password is not correctly comfirmed, please try again', category='error')
        else:

            #Add the new user to the database
            new_user_account = User(user_name = username,  
                                    email = email,
                                    password = generate_password_hash(password))

            db.session.add(new_user_account)
            db.session.commit()

            #login the new user
            flash(f'Login successful, welcome { username }', category='success')
            login_user(new_user_account)
            return redirect(url_for('views.home'))


    return render_template('sign_up.html')
