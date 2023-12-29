from flask import Flask, g
import logging, os
from flask_migrate import Migrate
from flask_login import LoginManager
from src.models import db
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['FOLDER_PARENT_STATIC'] = app.name
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder
os.makedirs(os.path.abspath(os.path.join(app.config['FOLDER_PARENT_STATIC'], upload_folder)), exist_ok=True)

from src.crud import *
from src.auth import *
from src.mail import *
from src.others import *
from src.routes import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def set_global_variables():
  g.site_title = "My active life"


# from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
# import config

# app = Flask(__name__)
# app.config.from_object(config.Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# api = Api(app)
# from src import models, routes
