import uuid
import random
import hashlib
from datetime import datetime
from secrets import token_hex
# from flask_script import Manager                          #FLASK_SCRIPT
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginIn, accountForm
from jinja2 import Template, Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, redirect, flash, session


app = Flask('__name__', template_folder='templates')
app.config['SECRET_KEY'] = token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:pass@localhost:5433/userDB'

#FLASK_SCRIPT
# app.debug = True
# manager = Manager(app)

db = SQLAlchemy(app)
unique_key = str(uuid.uuid4()).replace('-','')
__USER = None

class UserPost(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column( db.String( 255 ), nullable=False, unique=True )
    userpassword = db.Column(db.String(255), nullable=False)
    useremail = db.Column( db.String( 255 ), nullable=False)
    userdateofbirth = db.Column( db.DateTime(), default=datetime.utcnow )

    def __repr__(self):
        return "<{}:{}>".format( self.id, self.title[:10] )

@app.route('/', methods=['GET', 'POST'])
def indexPage():
    message = request.args.get('message')
    username = request.args.get('username')
    return render_template('index.html', message=message, username=username)

@app.route('/registration', methods=['GET', 'POST'])
def registrationUser():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        userData = UserPost(
            userid=random.randint( 100000, 999999 ),
            username = form.username.data,
            userpassword= hashlib.sha512(bytes(form.userpassword.data, 'utf-8')).hexdigest(),
            useremail = form.useremail.data,
            userdateofbirth = form.userdateofbirth.data
        )
        if db.session.query(UserPost.username).filter(UserPost.username == userData.username).all():
            flash( message='Name already exists' )
        else:
            tmp = userData.username
            db.session.add( userData )
            db.session.commit()
            db.session.close( )
            # return render_template('index.html', message='Registred', username=tmp)
            return redirect(url_for('indexPage', message='Registred', username=tmp))

    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginUser():
    form = LoginIn(request.form)
    if request.method == 'POST':
        userData = UserPost(
            username = form.username.data,
            userpassword = hashlib.sha512(bytes(form.userpassword.data, 'utf-8')).hexdigest()
        )
        try:
            userD = db.session.query( UserPost.username, UserPost.userpassword, UserPost.userid ) \
                .filter(UserPost.username == userData.username ).all( )
            if userD[0][0] and userD[0][1] == userData.userpassword:
                flash( message='correct' )
                session['userid'] = userD[0][2]
                return redirect( url_for( 'account' ) )
                # return redirect( url_for( 'jinjatest' ) )
            else:
                flash( message='Incorrect username or password' )
        except IndexError:
            flash( message='Incorrect username or password' )
    return render_template('login.html', form=form)

@app.route('/acc')
def account():
    try:
        innerUserid = session['userid']
        session.clear( )
        userD = db.session.query(UserPost.username,UserPost.useremail,UserPost.userdateofbirth).filter(UserPost.userid == innerUserid).all()
        uLabels = ['Name', 'Email', 'Date of Birth']
        dictUserData = dict(zip(uLabels, userD[0]))
        return render_template('account', uData=dictUserData)
    except KeyError:
        return 'Page not found', 404

@app.route('/jin')
def jinjatest():
    try:
        innerUserid = session['userid']
        session.clear( )
        userD = db.session.query( UserPost.username, UserPost.useremail, UserPost.userdateofbirth ).filter(
            UserPost.userid == innerUserid ).all( )
        uLabels = ['Name', 'Email', 'Date of Birth']
        dictUserData = dict( zip( uLabels, userD[0] ) )
        environment = Environment(loader=FileSystemLoader('templates/'))
        template = environment.get_template('jinja.html')
        content = template.render( userDict = dictUserData)
        return content
    except KeyError:
        return 'Page not found', 404

# if __name__ == '__main__':
#     manager.run()