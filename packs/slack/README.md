# Slack Integration Pack

Pack which allows integration with [Slack](https://slack.com/) service.

## Configuration

* ``post_message_action.webhook_url`` - Webhook URL.
* ``post_message_action.channel`` - Channel to send the message to (e.g.
  `#mychannel`). If not specified, messages will be sent to the channel which
  is selected when configuring a webhook.
* ``post_message_action.username`` - Default name of the user under which the
  messages will be posted. This setting can be overridden on per action basis.
* ``post_message_action.icon_emoji`` - Default icon of the user under which the
  messages will be posted. This setting can be overridden on per action basis.
  If not provided, default value which is selected when configuring a webhook
  is used.
* ``sensor.token`` - Authentication token used to authenticate against Real
  Time Messaging API.
* ``sensor.strip_formatting`` - By default, Slack automatically parses URLs, images,
  channels, and usernames. This option removes formatting and only returns the raw
  data from the client (URL only today)

### Obtaining a Webhook URL

To configure a webhook and obtain a URL, go to
https://[your company].slack.com/services/new/incoming-webhook, select a
channel you would like the messages to be posted to and click on "Add
Incoming WebHooks Integration" button.

![Step 1](/_images/slack_generate_webhook_url_1.png)

On the next page you will find an automatically generated webhook URL.

![Step 2](/_images/slack_generate_webhook_url_2.png)

### Obtaining Auth Token

To obtain a token for a production use, you should follow the instructions on
the following page - [OAuth - User
Authentication](https://api.slack.com/docs/oauth).

For testing purposes, you can use the same token as your browser based client
uses.

This is a lot simpler than going through the whole oAuth flow, but because of
the obvious security reasons and a temporary natural of the token, you should
only use that token for testing and debugging

To do that, navigate to your Slack instance, open Chrome developer console,
go to `Network` tab, filter on `XHR` requests and refresh the page. Find a
request to `file.list` or a similar endpoint and in the right page, under the
`Form Data` section you will see auth token your client uses to authenticate.

![Chrome developer console](/_images/slack_obtain_test_auth_token.png)

## Sensors

### SlackSensor

Slack sensor monitors Slack for activity and dispatches a trigger for each
message which is posted to a channel.

#### slack.message trigger

Example trigger payload:

```json
{
    "user": {
        "first_name": "Tomaz",
        "last_name": "Muraus",
        "is_owner": false,
        "name": "kami",
        "real_name": "Tomaz Muraus",
        "is_admin": false,
        "id": "U0CCCCC"
    },
    "channel": {
        "topic": "",
        "id": "C0CCCCCC",
        "name": "test"
    },
    "timestamp": 1419164091,
    "timestamp_raw": "1419164091.00005",
    "text": "This is a test message."
}
```

## Actions

* ``post_message`` - Action which posts a message to the channel using an
  incoming webhook.
