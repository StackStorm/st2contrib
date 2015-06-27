# pylint: disable=super-on-old-class
import time
import random

import eventlet
from irc.bot import SingleServerIRCBot

from st2reactor.sensor.base import Sensor

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)


class StackStormSensorBot(SingleServerIRCBot):
    def __init__(self, server_host, server_port, nickname, channels, handlers, logger):
        server_list = [(server_host, server_port)]
        super(StackStormSensorBot, self).__init__(server_list=server_list, nickname=nickname,
                                                  realname=nickname)
        self._channels = channels
        self._handlers = handlers
        self._logger = logger

    def on_welcome(self, connection, event):
        self._logger.debug('Connected to the server')

        for channel in self._channels:
            self._logger.debug('Joining #%s...' % (channel))
            connection.join(channel)

    def on_nicknameinuse(self, connection, event):
        new_nickname = '%s-%s' % (connection.get_nickname(), random.randint(1, 1000))
        connection.nick(new_nickname)

    def on_pubmsg(self, connection, event):
        event.timestamp = int(time.time())
        handler = self._handlers.get('pubmsg', lambda connection, event: connection)
        handler(connection=connection, event=event)

    def on_privmsg(self, connection, event):
        event.timestamp = int(time.time())
        handler = self._handlers.get('privmsg', lambda connection, event: connection)
        handler(connection=connection, event=event)

    def on_join(self, connection, event):
        event.timestamp = int(time.time())
        handler = self._handlers.get('join', lambda connection, event: connection)
        handler(connection=connection, event=event)

    def on_part(self, connection, event):
        event.timestamp = int(time.time())
        handler = self._handlers.get('part', lambda connection, event: connection)
        handler(connection=connection, event=event)


class IRCSensor(Sensor):
    def __init__(self, sensor_service, config=None):
        super(IRCSensor, self).__init__(sensor_service=sensor_service,
                                        config=config)
        self._logger = self._sensor_service.get_logger(__name__)

        split = self._config['server'].split(':')
        self._server_host = split[0]
        self._server_port = int(split[1])
        self._nickname = self._config['nickname']
        self._channels = self._config['channels']

    def setup(self):
        handlers = {
            'pubmsg': self._handle_pubmsg,
            'privmsg': self._handle_privmsg,
            'join': self._handle_join,
            'part': self._handle_part
        }
        self._bot = StackStormSensorBot(server_host=self._server_host,
                                        server_port=self._server_port,
                                        nickname=self._nickname, channels=self._channels,
                                        handlers=handlers,
                                        logger=self._logger)

    def run(self):
        self._bot.start()  # pylint: disable=no-member

    def cleanup(self):
        self._bot.disconnect(msg='Disconnecting')  # pylint: disable=no-member

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _handle_pubmsg(self, connection, event):
        trigger = 'irc.pubmsg'

        payload = {
            'source': {
                'nick': event.source.nick,
                'host': event.source.host
            },
            'channel': event.target,
            'timestamp': event.timestamp,
            'message': event.arguments[0]
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _handle_privmsg(self, connection, event):
        trigger = 'irc.privmsg'
        payload = {
            'source': {
                'nick': event.source.nick,
                'host': event.source.host
            },
            'timestamp': event.timestamp,
            'message': event.arguments[0]
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _handle_join(self, connection, event):
        trigger = 'irc.join'
        payload = {
            'source': {
                'nick': event.source.nick,
                'host': event.source.host
            },
            'timestamp': event.timestamp,
            'channel': event.target
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _handle_part(self, connection, event):
        trigger = 'irc.part'
        payload = {
            'source': {
                'nick': event.source.nick,
                'host': event.source.host
            },
            'timestamp': event.timestamp,
            'channel': event.target
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
