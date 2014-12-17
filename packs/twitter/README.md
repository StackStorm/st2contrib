# Twitter Integration Pack

Pack which allows integration with Twitter.

## Configuration

* ``consumer_key`` - Twitter API consumer key
* ``consumer_secret`` - Twitter API consumer secret
* ``access_token`` - Twitter API access token
* ``access_token_secret`` - Twitter API access token secret

* ``keywords`` - A list of keyword to search the Twitter timeline for
* ``language`` - If specified, only return tweets in the provided language

## Sensors

### TwitterSearchSensor

This sensor searches Twitter for recent tweets matching the criteria defined in
the config. When a matching Tweet is found, a trigger is dispatcher.
