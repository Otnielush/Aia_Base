from flask import (
    url_for,
    render_template,
    redirect,
make_response
)
from facebook_scraper import get_posts, get_group_info
import re

def init_test(app):

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        """User sign-up form for account creation."""



    @app.route("/test")
    def users():

        return make_response(
            'Test worked!',
            200,
        )


    return app

print(get_group_info('avodot'))
