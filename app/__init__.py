from flask import Flask
from flask_redis import FlaskRedis
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['REDIS_URL'] = "redis://localhost:6379/0"
redis_store = FlaskRedis(app)
Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes
