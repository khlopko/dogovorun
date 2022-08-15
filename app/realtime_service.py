import gevent


class RealtimeService:

    def __init__(self, redis, channel):
        self.clients = []
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(channel)
        self.app = None

    def init_app(self, app):
        self.app = app

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                self.app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)


def register_routes(app, sockets, redis, channel, service):
    @sockets.route('/submit')
    def inbox(ws):
        while not ws.closed:
            gevent.sleep(0.01)
            message = ws.receive()
            if message:
                app.logger.info(u'Inserting message: {}'.format(message))
                redis.publish(channel, message)

    @sockets.route('/receive')
    def outbox(ws):
        service.register(ws)
        while not ws.closed:
            gevent.sleep(0.01)
