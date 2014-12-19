# Slack Integration Pack

Pack which allows integration with [Slack](https://slack.com/) service.

## Configuration

* ``webhook_url`` - Webhook URL.
* ``username`` - Default name of the user under which the messages will be
  posted. This setting can be overridden on per action basis.
* ``icon_emoji`` - Default icon of the user under which the messages will be
  posted. This setting can be overridden on per action basis.

### Obtaining a Webhook URL

To configure a webhook and obtain a URL, go to
https://<your company>.slack.com/services/new/incoming-webhook, select a
channel you would like the messages to be posted to and click on "Add
Incoming WebHooks Integration" button.

![Step 1](/_images/slack_generate_webhook_url_1.png)

On the next page you will find an automatically generated webhook URL.

![Step 2](/_images/slack_generate_webhook_url_2.png)

## Actions

* ``post_message`` - Action which posts a message to the channel using an
  incoming webhook.
