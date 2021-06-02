from flask import render_template, request
from .forms import LoginForm, SignupForm

from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user

from .models import db, User
from .. import login_manager

def init_auth(app):
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """
        User sign-up page.

        GET requests serve sign-up page.
        POST requests validate form & user creation.
        """
        form = SignupForm()
        if form.validate_on_submit():
            # User sign-up logic will go here.
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    phone=form.phone.data
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()  # Create new user
                login_user(user)  # Log in as newly created user
                return redirect(url_for('/'))
            flash('A user already exists with that email address.')
        return render_template(
            'signup.jinja2',
            title='Create an Account.',
            form=form,
            template='signup-page',
            body="Sign up for a user account."
        )

    return app