import os
from datetime import timedelta

import redis
from flask import Flask
from flask_cors import CORS
from flask_sockets import Sockets

from .realtime_service import RealtimeService, register_routes
from .store.file_game_gateway import FileGameGateway

sockets = Sockets()

REDIS_CHANNEL = 'game'
redis = redis.from_url(os.environ['REDIS_URL'])
rs = RealtimeService(redis=redis, channel=REDIS_CHANNEL)


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
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

    from .views.api import api
    app.register_blueprint(blueprint=api)

    from app.views.api import register_error_handlers
    register_error_handlers(app=app)

    sockets.init_app(app=app)
    rs.init_app(app=app)
    rs.start()
    register_routes(app=app, sockets=sockets, redis=redis, channel=REDIS_CHANNEL, service=rs)

    return app
