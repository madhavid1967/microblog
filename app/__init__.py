from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from models import User

@lm.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
from app import views, models, queries