# Twitter Integration Pack

Pack which allows integration with Twitter.

## Configuration

* ``consumer_key`` - Twitter API consumer key.
* ``consumer_secret`` - Twitter API consumer secret.
* ``access_token`` - Twitter API access token.
* ``access_token_secret`` - Twitter API access token secret.
* ``query`` - A query to search the twitter timeline for. You can use all the
  query operators described at https://dev.twitter.com/rest/public/search
* ``count`` - Number of latest tweets matching the criteria to retrieve.
  Defaults to 30, maximum is 100.
* ``language`` - If specified, only return tweets in the provided language.
  For example: `en`, `de`, `jp`, etc.

### Obtaining API credentials

To obtain API credentials, you need to first register your application on the
[Twitter Application Management](https://apps.twitter.com/) page.

![Step 1](/_images/twitter_create_app.png)

After you have done that, go to the `Keys and Access Tokens` tab where you can
find your consumer key and secret. On the same page you can also generate an
access token (click on the ``Create my access token`` button).

![Step 2](/_images/twitter_obtain_consumer_key.png)

For the sensor a "Read only" token is sufficient, but for the action you need
to use a token with a "Read and Write" access.

![Step 3](/_images/twitter_create_access_token.png)

![Step 4](/_images/twitter_obtain_access_token.png)

## Sensors

### TwitterSearchSensor

This sensor searches Twitter for recent tweets matching the criteria defined in
the config. When a matching Tweet is found, a trigger is dispatcher.

## Actions

* ``update_status`` - Action which updates your status / posts a new tweet.

## Rules

### relay_tweet_to_slack

Rule which shows how to relay every matched tweet to the Slack channel.
