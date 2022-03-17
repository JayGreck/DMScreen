from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_data.db'
app.config['SECRET_KEY'] = '28f621d1db1fee74cef4bc6cc0dce5f4'
# Initialize database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Redirects to login page if unauthorized access occurs
login_manager.login_message_category = 'info'

from flaskdmscreen import routes

db.create_all()