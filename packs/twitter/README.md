# Twitter Integration Pack

Pack which allows integration with Twitter.

## Configuration

* ``consumer_key`` - Twitter API consumer key
* ``consumer_secret`` - Twitter API consumer secret
* ``access_token`` - Twitter API access token
* ``access_token_secret`` - Twitter API access token secret
* ``query`` - A query to search the twitter timeline for. You can use all the
  query operators described at https://dev.twitter.com/rest/public/search
* ``count`` - Number of latest tweets matching the criteria to retrieve.
  Defaults to 30, maximum is 100.
* ``language`` - If specified, only return tweets in the provided language

## Sensors

### TwitterSearchSensor

This sensor searches Twitter for recent tweets matching the criteria defined in
the config. When a matching Tweet is found, a trigger is dispatcher.
