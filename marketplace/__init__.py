from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea05b6e38431cd809ac9652400549700'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'

db = SQLAlchemy(app)
app.app_context().push()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from marketplace import routes
