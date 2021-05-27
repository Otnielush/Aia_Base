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
    URL
)

# TODO https://developers.google.com/recaptcha/docs/display    RECAPTCHA
# RecaptchaField is a field type specific to Flask-WTF (hence why we import it from flask_wtf instead of wtforms).
# As you may expect, this allows us to add a captcha to our form to prevent bots from submitting forms.
# A valid Recaptcha field requires us to supply two configuration variables to work:
# RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ]
    )
    body = TextField(
        'Message',
        [
            DataRequired(),
            Length(min=4,
            message=('Your message is too short.'))
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    """Sign up for a user account."""
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )
    confirmPassword = PasswordField(
        'Repeat Password',
        [
            EqualTo(password, message='Passwords must match.')
        ]
    )
    title = SelectField(
        'Title',
        [DataRequired()],
        choices=[
            ('Farmer', 'farmer'),
            ('Corrupt Politician', 'politician'),
            ('No-nonsense City Cop', 'cop'),
            ('Professional Rocket League Player', 'rocket'),
            ('Lonely Guy At A Diner', 'lonely'),
            ('Pokemon Trainer', 'pokemon')
        ]
    )
    website = StringField(
        'Website',
        validators=[URL()]
    )
    birthday = DateField('Your Birthday')
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

