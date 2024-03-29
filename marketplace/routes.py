from marketplace import app, db
from flask import render_template, redirect, url_for, flash, request
from marketplace.models import Item, User
from marketplace.forms import RegistrationForm, LoginForm, PurchaseItemForm, SellItemForm, ItemForm, UpdateItemForm, DeleteItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', title='Welcome')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    updateitem_form = UpdateItemForm()
    deleteitem_form = DeleteItemForm()
    if request.method == "POST":
        #Purchase Logic
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f'Congratulations! You purchased {purchased_item_object.name} for ${purchased_item_object.price}', category='success')
            else:
                flash(f"Sorry, you don't have enough money to purchase {purchased_item_object.name}!", category='danger')
                
        #Sell Logic
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f'Congratulations! You sold {sold_item_object.name} for ${sold_item_object.price}', category='success')
            else:
                flash(f"Something went wrong with selling {sold_item_object.name}!", category='danger')
        
        #Update Item Logic
        update_item = request.form.get('update_item')
        update_item_object = Item.query.filter_by(id=update_item).first()
        if update_item_object:
            if updateitem_form.validate_on_submit():
                update_item_object.name = updateitem_form.name.data
                update_item_object.price = updateitem_form.price.data
                update_item_object.description = updateitem_form.description.data
                db.session.commit()
                flash(f'You update product {update_item_object.name}', category='success')
        
        #Delete Logic
        delete_item = request.form.get('delete_item')
        delete_item_object = Item.query.filter_by(id=delete_item).first()
        if delete_item_object:
            db.session.delete(delete_item_object)
            db.session.commit()
            flash(f'You have just delete {delete_item_object.name} from your owned items', category='danger')
        return redirect(url_for('market_page'))
    
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', title='Market', items=items, purchase_form=purchase_form, selling_form=selling_form, updateitem_form=updateitem_form, deleteitem_form=deleteitem_form, owned_items=owned_items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')
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
            login_user(attempted_user, remember=form.remember.data)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Email and Password are not match! Please retry', category='warning')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')
    return redirect(url_for('home_page'))

@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        user_to_post = Item(name=form.name.data, description=form.description.data, price=form.price.data, owner=current_user.id)
        db.session.add(user_to_post)
        db.session.commit()
        flash(f'Congratulations! You add: {user_to_post.name}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #Validation error handling
        for err_msg in form.errors.values():
            flash(f'Post Item Error: {err_msg}', category='warning')
    return render_template('create_item.html', title='New Item', form=form)
        

