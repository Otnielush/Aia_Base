from os import path
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
login_manager = LoginManager()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('application.database.config.DevConfig')

    # Request limiter
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["10000 per day", "3000 per hour", "1/second"]
    )

    # Initialize Plugins
    db.init_app(app)
    # login_manager.init_app(app)



    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

    from application.funcs.whatsapp import Whatsapp
    app.whatsapp = Whatsapp()
    # from application.funcs.instagram_post import Instagram
    # app.instagram = Instagram()

    from application.funcs.workers import init_workers
    app = init_workers(app)
    from application.funcs.clients import init_clients
    app = init_clients(app)
    from application.funcs.jobs import init_jobs
    app = init_jobs(app)
    from application.funcs.errors import init_errors
    app = init_errors(app)
    from application.funcs.fb_scraper import init_fb_scraper; app = init_fb_scraper(app)
    from application.funcs.test import init_test; app = init_test(app)
    # from application.funcs.auth import init_auth; app = init_auth(app)

    app.lang = 'rus'

    # Create Database Models
    # db.create_all()

    # app.config.from_object('application.database.config.ProdConfig')

    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)

    return app





