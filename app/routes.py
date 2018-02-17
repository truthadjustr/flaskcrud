import datetime
from app import app,redis_store
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
    session,\
    flash

ACCESS_CONTROL = {
    'johnny':'password1',
    'mary':'password2',
}

@app.route('/')
@app.route('/index')
def index():
    user = session.get('loginusername',None)
    if user and redis_store.exists('loginusername:' + user):
        return render_template('index.html',user=user,isactive=True)
    return render_template('index.html',user=user,isactive=False)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('loginusername')
        password = request.form.get('loginpassword')
        if ACCESS_CONTROL.get(user,None) and password == ACCESS_CONTROL[user]:
            if not redis_store.exists('loginusername:' + user):
                session['loginusername'] = user
                redis_store.setex('loginusername:' + user,60,datetime.datetime.now())
                return redirect(url_for('content'))
            flash("User {} is currently logged in another session".format(user))
    if 'loginusername' not in session:
        return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'loginusername' in session:
        redis_store.delete('loginusername:' + session['loginusername'])
        session.pop('loginusername')
    return redirect(url_for('index'))

@app.route('/content',methods=['GET','POST'])
def content():
    if request.method == 'POST':
        var1 = request.form.get('conf')
        if var1 == 'running':
            print("PARAM = " + var1)
    user = session.get('loginusername',None)
    if user and redis_store.exists('loginusername:' + user):
        return render_template('content.html',user=user,isactive=True)
    return redirect(url_for('index'))

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        config = request.args.get('conf')
        print("config = " + config)
        if config:
            print("applyto " + config)
    return redirect(url_for('content'))

@app.before_request
def before_request():
    user = session.get('loginusername',None)
    if user:
        # if browser session exists, but the timeout expires, then 
        # logout the user
        if not redis_store.exists('loginusername:' + user):
            session.pop('loginusername')
        else:
            # else, reset the timeout since there is
            # browser activity
            redis_store.setex('loginusername:' + user,60,datetime.datetime.now())
