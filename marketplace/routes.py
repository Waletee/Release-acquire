from marketplace import app, db
from flask import render_template, redirect, url_for, flash
from marketplace.models import Item, User
from marketplace.forms import RegistrationForm, LoginForm
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', title='Market', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #Validation error handling
        for err_msg in form.errors.values():
            flash(f'Registration Error: {err_msg}', category='warning')
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Email and Password are not match! Please retry', category='warning')
    return render_template('login.html', title='Login', form=form)
