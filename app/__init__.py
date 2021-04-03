import os
from datetime import timedelta

from flask import Flask

from .store import FileGameGateway


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        GAMES_PATH=os.path.join(app.instance_path, 'games'),
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=60*24)
    )

    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .views import bp
    app.register_blueprint(bp)

    return app
