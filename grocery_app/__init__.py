from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from grocery_app.models import User

app = Flask(__name__)

# Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


# -----------------------
# User Loader
@login_manager.user_loader
def load_user(user_id):
    """Load user"""
    return User.query.get(int(user_id))

bcrypt = Bcrypt(app)
bcrypt.init_app(app)
