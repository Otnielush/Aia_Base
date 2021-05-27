from os import path
from flask import Flask, send_from_directory



def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('application.database.config.DevConfig')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

    from application.funcs.whatsapp import Whatsapp
    app.whatsapp = Whatsapp()

    from application.funcs.workers import init_workers
    app = init_workers(app)
    from application.funcs.clients import init_clients
    app = init_clients(app)
    from application.funcs.jobs import init_jobs
    app = init_jobs(app)
    from application.funcs.errors import init_errors
    app = init_errors(app)
    from application.funcs.test import init_test
    app = init_test(app)

    app.lang = 'rus'


    # app.config.from_object('application.database.config.ProdConfig')

    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)

    return app





