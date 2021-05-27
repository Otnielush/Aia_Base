from flask import render_template, make_response
from .language import lang_select


def init_errors(app):

    @app.errorhandler(404)
    def not_found():
        """Page not found."""
        msg='Page not found.'
        # Lang selector
        _, button_names = lang_select(app.lang)
        return make_response(
            render_template('result.html', msg=msg, b_names=button_names, autolink='/'),
            404)


    @app.errorhandler(400)
    def bad_request():
        """Bad request."""
        msg='Bad request.'
        # Lang selector
        _, button_names = lang_select(app.lang)
        return make_response(
            render_template('result.html', msg=msg, b_names=button_names, autolink='/'),
            400)


    @app.errorhandler(500)
    def server_error():
        """Internal server error."""
        msg='Internal server error.'
        # Lang selector
        _, button_names = lang_select(app.lang)
        return make_response(
            render_template('result.html', msg=msg, b_names=button_names, autolink='/'),
            500)

    return app

