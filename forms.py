from wtforms.validators import DataRequired, Email
from wtforms import Form, StringField, SubmitField, TextAreaField, DateField, validators, EmailField, PasswordField, IntegerField


class RegistrationForm(Form):
    username = StringField( 'Name ', [DataRequired( ), validators.Length( min=4, max=25 )] )
    useremail = EmailField( 'Email ', [DataRequired(), validators.Email( ), validators.Length( min=4, max=35 )] )
    #userpassword = PasswordField( 'Password ', [DataRequired(), validators.Length( min=5, max=30 )] )
    userpassword = StringField( 'Password ', [DataRequired( ), validators.Length( min=5, max=30 )] )
    userdateofbirth = DateField('Date of Birth ', format='%Y-%m-%d')
    submit = SubmitField( 'Submit' )


class LoginIn(Form):
    username = StringField( 'Name ', [DataRequired( ), validators.Length( min=4, max=25 )] )
    #userpassword = PasswordField( 'Password ', [DataRequired(), validators.Length( min=5, max=30 )] )
    userpassword = StringField( 'Password ', [DataRequired( ), validators.Length( min=5, max=30 )] )
    submit = SubmitField( 'Submit' )

class accountForm(Form):
    username = StringField( 'Name ', [DataRequired( ), validators.Length( min=4, max=25 )] )
    useremail = EmailField( 'Email ', [DataRequired( ), validators.Email( ), validators.Length( min=4, max=35 )] )
    userdateofbirth = DateField( 'Date of Birth ', format='%Y-%m-%d' )
    userid = IntegerField('ID')