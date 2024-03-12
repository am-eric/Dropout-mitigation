from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import User
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user


bcrypt = Bcrypt()


from . import db



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        #check password
        user = User.query.filter_by(email=email).first() #query database by specific field 
        if user:
            if bcrypt.check_password_hash(user.password, password):
                flash('logged in Successfuly', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                # User not found or incorrect password
                flash('Login failed. Check your email and password.', category='error')
        else:
            flash ('Email doea not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() #query database by specific field


        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('Name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))


    # Redirect to the same page, so that flashed messages can be displayed
    return render_template('sign_up.html', user=current_user)
