import uuid
import random
import hashlib

import psycopg2
import sqlalchemy.exc
from datetime import datetime
from secrets import token_hex
# from flask_script import Manager                          #FLASK_SCRIPT
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginIn, accountForm, sqlForm
from jinja2 import Template, Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, redirect, flash, session

app = Flask('__name__', template_folder='C:/Users/INSAGNIFICANT/PycharmProjects/flaskLogin/templates')
app.config['SECRET_KEY'] = token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:pass@localhost:5433/userDB'
app.config['EXPLAIN_TEMPLATE_LOADING'] = False

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
        return "<UserPost(username='%s', userpassword='%s', useremail='%s', userdateofbirth='%s )>" % (
            self.username, self.userpassword, self.useremail, self.userdateofbirth)

    def setPassword(self, password):
        self.userpassword = password


@app.route('/', methods=['GET', 'POST'])
def indexPage():
    if request.args:
        return render_template('index.html', message=request.args.get('message'), username=request.args.get('username'))
    return render_template( 'index.html' )

def checkUserId(userid, db):
    if userid not in db:
        return userid
    userid = random.randint( 100000, 999999)
    return checkUserId(userid, db)

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
        usersIdListTemp = db.session.query(UserPost.userid).all()
        usersIdList = []
        for i in usersIdListTemp:
            usersIdList.append(i)
        userData.userid = checkUserId(userData.userid, usersIdList)
        usersIdList.clear()
        usersIdListTemp.clear()
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
        except (IndexError, TypeError):
            flash( message='Incorrect username or password' )
        except sqlalchemy.exc.OperationalError:
            flash( message='DB error')
    return render_template('login.html', form=form)

@app.route('/acc')
def account():
    try:
        innerUserid = session['userid']
        session.clear( )
        userD = db.session.query(UserPost.username,UserPost.useremail,UserPost.userdateofbirth).filter(UserPost.userid == innerUserid).all()
        uLabels = ['Name', 'Email', 'Date of Birth']
        dictUserData = dict(zip(uLabels, userD[0]))
        session['userid'] = innerUserid
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

@app.route('/choic/<func>')
def choicefunc(func):
    if func == 'setPassword':
        session['func'] = func
        return redirect(url_for('varpage'))
    elif func == 'doSQLquery':
        session['func'] = func
        return redirect(url_for('varpage'))
    else:
        return 'page not found'

@app.route('/varpagetto', methods=['GET','POST'])
def varpage():
    try:
        if session['func'] == 'setPassword':
            form = LoginIn( request.form )
            if request.method == 'POST':
                if request.form.get( 'password' ) == request.form.get( 'passwordRe' ):
                    userData = UserPost.query.filter_by(userid = session['userid']).first()
                    userData.setPassword(hashlib.sha512(bytes(request.form.get('password'),'utf-8')).hexdigest())
                    db.session.commit()
                    flash(message='password changed')
                    session.clear( )
                    return render_template('index.html', pagename='Change password', form=form)
                else:
                    message = 'Passwords don\'t match'
                    session.clear( )
                    return render_template( 'varpage.html', pagename='Change password', form=form, message=message)
            return render_template('varpage.html', pagename='Change password', form=form)
        elif session['func'] == 'doSQLquery': # select username, useremail from users
            try:
                form = sqlForm( request.form )
                if request.method == 'POST':
                    query = form.sqlquery.data
                    queryResult = db.session.execute(text(query))
                    records = [(num+1, *rec) for num,rec in enumerate(queryResult)]
                    session.clear( )
                    return render_template( 'varpage.html', pagename='do SQL query', form=form, records=records, lenRecords=range(1,len(records)+1) )
                return render_template('varpage.html', pagename='do SQL query', form=form)
            except sqlalchemy.exc.ProgrammingError as err:
                message = 'SQL query error.\r\n' + str(err)
                return render_template('varpage.html', pagename='do SQL query', form=form, message=message)
    except KeyError:
        return 'Wrong session'

# if __name__ == '__main__':
#     manager.run()
