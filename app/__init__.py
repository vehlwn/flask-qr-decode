import flask
import flask_bootstrap
import os
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = flask_bootstrap.Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/main")
    return app
