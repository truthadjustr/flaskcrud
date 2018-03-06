import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_redis import FlaskRedis
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['bin'])

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
redis_store = FlaskRedis(app)
Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'


from app import routes
