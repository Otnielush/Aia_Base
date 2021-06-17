from flask import (
    url_for,
    render_template,
    redirect,
    make_response,
    request,
g
)
from facebook_scraper import get_posts, get_group_info
import re

def init_test(app):

    @app.route("/test")
    def new_test():

        # return render_template('test.html', next='u will be next')
        return redirect(url_for("workers", q='נתניה'), code=302)
        # return make_response(
        #     "url: "+ str(request.url) + '; Test worked!',
        #     200,
        # )



    return app

