from app import app
from flask_login import \
    current_user, \
    login_user, \
    logout_user,\
    login_required
from flask import \
    render_template,\
    request,\
    redirect,\
    url_for,\
    session

ACCESS_CONTROL = {
    'johnny':'password1',
    'mary':'password2',
}

@app.route('/')
@app.route('/index')
def index():
    user = session.get('xxx',None)
    return render_template('index.html',user=user)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('xxx')
        password = request.form.get('yyy')
        if ACCESS_CONTROL.get(user,None) and password == ACCESS_CONTROL[user]:
            session['xxx'] = user
            return redirect(url_for('content'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('xxx')
    return redirect(url_for('index'))

@app.route('/content')
def content():
    user = session.get('xxx',None)
    if user:
        return render_template('content.html',user=user)
    return redirect(url_for('index'))
