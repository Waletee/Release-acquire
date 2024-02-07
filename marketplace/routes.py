from marketplace import app, db
from flask import render_template, redirect, url_for
from marketplace.models import Item, User
from marketplace.forms import RegistrationForm, LoginForm

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
        user_to_create = User(username=form.username.data, email=form.email.data, password_hashed=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #Validation error handling
        for err_msg in form.errors.values():
            print(f'There is an error creating a user: {err_msg}')
    return render_template('register.html', title='Registration', form=form)

@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
