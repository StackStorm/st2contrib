# pylint: disable=super-on-old-class
import random

import eventlet
from irc.bot import SingleServerIRCBot

from st2actions.runners.pythonrunner import Action

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=True,
    time=True)

__all__ = [
    'PostMessageAction'
]


class StackStormActionIRCBot(SingleServerIRCBot):
    def __init__(self, server_host, server_port, nickname, channel, message):
        server_list = [(server_host, server_port)]
        super(StackStormActionIRCBot, self).__init__(server_list=server_list,
                                                     nickname=nickname,
                                                     realname=nickname)
        self._channel = channel
        self._message = message

    def on_welcome(self, connection, event):
        try:
            connection.join(self._channel)
            self.connection.privmsg(self._channel, self._message)  # pylint: disable=no-member
        finally:
            self.die(msg='Disconnecting')  # pylint: disable=no-member

    def on_nicknameinuse(self, connection, event):
        new_nickname = '%s-%s' % (connection.get_nickname(), random.randint(1, 1000))
        connection.nick(new_nickname)


class PostMessageAction(Action):
    def run(self, channel, message):
        bot = self._get_bot(channel=channel, message=message)
        bot.start()  # pylint: disable=no-member

        return True

    def _get_bot(self, channel, message):
        split = self.config['server'].split(':')
        server_host = split[0]
        server_port = int(split[1])
        nickname = self.config['nickname']
        bot = StackStormActionIRCBot(server_host=server_host,
                                     server_port=server_port,
                                     nickname=nickname,
                                     channel=channel,
                                     message=message)
        return bot
