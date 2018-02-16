from app import app
from flask_login import \
    current_user, \
    login_user, \
    logout_user,\
    login_required
from flask import \
    render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')