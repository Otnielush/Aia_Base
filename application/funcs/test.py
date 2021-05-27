from flask import (
    url_for,
    render_template,
    redirect,
make_response
)
from .test_dir.forms import ContactForm, SignupForm

def init_test(app):

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        """Standard `contact` form."""
        form = ContactForm()
        if form.validate_on_submit():
            print('con val')
            return redirect(url_for("success"))
        return render_template(
            "contact.jinja2",
            form=form,
            template="form-template"
        )

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        """User sign-up form for account creation."""
        form = SignupForm()
        if form.validate_on_submit():
            print('sing val')
            return redirect(url_for("users"))
        return render_template(
            "signup.jinja2",
            form=form,
            template="form-template",
            title="Signup Form"
        )

    @app.route("/api/test")
    def users():
        headers = {"Content-Type": "application/json"}
        return make_response(
            'Test worked!',
            200,
        )

    @app.route("/login")
    def login():
        return redirect(url_for('signup'))  # name of function for routing

    return app