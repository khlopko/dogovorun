import os
from datetime import timedelta

import gevent
import redis
from flask import Flask
from flask_sockets import Sockets

from .realtime_service import RealtimeService
from .store import FileGameGateway

sockets = Sockets()

REDIS_CHANNEL = 'game'
redis = redis.from_url(os.environ['REDIS_URL'])
rs = RealtimeService(redis=redis, channel=REDIS_CHANNEL)


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

    sockets.init_app(app)
    rs.init_app(app)

    rs.start()

    @sockets.route('/submit')
    def inbox(ws):
        """Receives incoming chat messages, inserts them into Redis."""
        while not ws.closed:
            # Sleep to prevent *contstant* context-switches.
            gevent.sleep(0.1)
            message = ws.receive()

            if message:
                app.logger.info(u'Inserting message: {}'.format(message))
                redis.publish(REDIS_CHANNEL, message)

    @sockets.route('/receive')
    def outbox(ws):
        """Sends outgoing chat messages, via `ChatBackend`."""
        rs.register(ws)

        while not ws.closed:
            # Context switch while `ChatBackend.start` is running in the background.
            gevent.sleep(0.1)

    return app
