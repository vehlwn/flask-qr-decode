import flask
import flask_bootstrap
import os

import config

bootstrap = flask_bootstrap.Bootstrap()


def create_app(config_name):
    app = flask.Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)

    bootstrap.init_app(app)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    return app
