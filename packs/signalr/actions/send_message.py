from st2actions.runners.pythonrunner import Action
from signalr import Connection

__all__ = [
    'SignalRSendMessageAction'
]


class SignalRSendMessageAction(Action):
    def __init__(self, config=None):
        super(SignalRSendMessageAction, self).__init__(config=config)
        self.url = config['hub_url']
        self.session = None

    def run(self, hub, message):
        connection = Connection(self.url, self.session)
        connection.start()
        # get hub
        _hub = self.connection.hub(hub)
        _hub.server.invoke('send_message', message)
        connection.close()
