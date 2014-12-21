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
