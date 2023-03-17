from wtforms.validators import DataRequired
from wtforms import Form, StringField, SubmitField, DateField, validators, EmailField, IntegerField, TextAreaField


class RegistrationForm(Form):
    username = StringField( u'Name ', [DataRequired( ), validators.Length( min=4, max=25 )] )
    useremail = EmailField( u'Email ', [DataRequired(), validators.Email( ), validators.Length( min=4, max=35 )] )
    #userpassword = PasswordField( 'Password ', [DataRequired(), validators.Length( min=5, max=30 )] )
    userpassword = StringField( u'Password ', [DataRequired( ), validators.Length( min=5, max=30 )] )
    userdateofbirth = DateField(u'Date of Birth ', format='%Y-%m-%d')
    submit = SubmitField( 'Submit' )

class LoginIn(Form):
    username = StringField( u'Name ', [DataRequired( ), validators.Length( min=4, max=25 )] )
    #userpassword = PasswordField( 'Password ', [DataRequired(), validators.Length( min=5, max=30 )] )
    userpassword = StringField( u'Password ', [DataRequired( ), validators.Length( min=5, max=30 )] )
    userpasswordRe = StringField( u'Password ', [DataRequired( ), validators.Length( min=5, max=30 )] )
    submit = SubmitField( 'Submit' )

class accountForm(Form):
    username = StringField( u'Name ', [DataRequired( ), validators.Length( min=4, max=25 )] )
    useremail = EmailField( u'Email ', [DataRequired( ), validators.Email( ), validators.Length( min=4, max=35 )] )
    userdateofbirth = DateField( u'Date of Birth ', format='%Y-%m-%d' )
    userid = IntegerField('ID')

class sqlForm(Form):
    sqlquery = TextAreaField('Text')