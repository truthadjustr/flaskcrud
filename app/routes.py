import datetime
import os
from app import app,redis_store,secure_filename,ALLOWED_EXTENSIONS

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

from werkzeug.urls import url_parse

ACCESS_CONTROL = {
    'johnny':'password1',
    'mary':'password2',
}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods = ['GET','POST'])
#@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('index'))
    return render_template('upload.html',user=user,isactive=False)

@app.route('/')
@app.route('/index')
def index():
    print("** index **")
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

                #next_page = request.args.get('next')
                #print("** next_page = {}".format(next_page))
                #if not next_page or url_parse(next_page).netloc != '':
                #    print("*** NO NEXT PAGE detected ***")
                #    next_page = url_for('content')
                #return redirect(next_page)

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
