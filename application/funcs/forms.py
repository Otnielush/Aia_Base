"""Form object declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    TextField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    URL,
)

# TODO https://developers.google.com/recaptcha/docs/display    RECAPTCHA
# RecaptchaField is a field type specific to Flask-WTF (hence why we import it from flask_wtf instead of wtforms).
# As you may expect, this allows us to add a captcha to our form to prevent bots from submitting forms.
# A valid Recaptcha field requires us to supply two configuration variables to work:
# RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY

class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        [   DataRequired(),
            Email(message='Enter a valid email.') ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    """Sign up for a user account."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [Length(min=6),
         Email(message=('Not a valid email address.')),
         DataRequired()]
    )
    password = PasswordField(
        'Password',
        [ DataRequired(message="Please enter a password."),
          Length(min=6, message='Select a stronger password.') ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        [   DataRequired(),
            EqualTo('password', message='Passwords must match.') ]
    )
    phone = StringField(
        'phone number',
        [Length(min=10, max=13, message="Not match to Israel's phone number")]
    )

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

