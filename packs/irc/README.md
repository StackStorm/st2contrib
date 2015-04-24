# IRC Integration Pack

Pack which allows integration with Internet Relay Chat (IRC).

## Configuration

* ``nickname`` - Bot nickname.
* ``server`` - Server to connect to in the `<hostname:port>` format. For
  example `irc.freenode.net:6667`.
* ``channels`` - A list of channels to join and monitor.

## Sensors

### IRCSensor

A sensor which dispatches an event for each public message which is sent to
any of the channel the bot is on and each private message which is sent
directly to the bot.

#### irc.pubmsg trigger

Dispatched when a message is posted to the channel.

Example trigger payload:

```json
{
    "source": {
        "nick": "Kami__",
        "host": "gateway/web/irccloud.com/x-uvv"
    },
    "channel": "#test989",
    "timestamp": 1419166748,
    "message": "this is a test message"
}
```

#### irc.privmsg trigger

Dispatched when a message is sent directly to the sensor bot.

Example trigger payload:

```json
{
    "source": {
        "nick": "Kami__",
        "host": "gateway/web/irccloud.com/x-uvv"
    },
    "timestamp": 1419166748,
    "message": "hello stackstorm!"
}
```

#### irc.join trigger

Dispatched when a user joins a channel.

Example trigger payload:

```json
{
    "source": {
        "nick": "Kami__",
        "host": "gateway/web/irccloud.com/x-uvv"
    },
    "channel": "#test989",
    "timestamp": 1419166748
}
```

#### irc.part trigger

Dispatched when a user parts a channel.

Example trigger payload:

```json
{
    "source": {
        "nick": "Kami__",
        "host": "gateway/web/irccloud.com/x-uvv"
    },
    "channel": "#test989",
    "timestamp": 1419166748
}
```

## Actions

* ``post_message`` - Action which sends a message to the specified IRC channel.
  The IRC server and bot nickname are specified in the config (see
  Configuration section above). Note: This action establish a new short-running
  connection to an IRC server for each action run. This approach has multiple
  limitations (it's slow, depends on server settings such as maximum number of
  connections per host, etc.)
