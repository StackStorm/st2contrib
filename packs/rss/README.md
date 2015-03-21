# RSS Integration Pack

## Sensors

### RSSSensor

This sensor periodically polls RSS / Atom feed for new entries and once a new
entry is detected, a trigger is emitted.

By default the sensor tries to filter out duplicated entries by using the entry
publish timestamp - a trigger is only emitted for entries with a timestamp
which is larger than the one we have last seen.

Keep in mind that this approach is not perfect and it's a compromise between
duplicated triggers and potentially missing some entries. Some blog post new
entries with a timestamp in the past - if timestamp based filtering is enabled,
those entries will be skipped.

TODO - this is sensor with parameters document how to configure it via cli

#### rss.entry trigger

Example trigger payload:

```json
{
    "feed": {
        "title": "StackStorm",
        "subtitle": "Event-driven automation",
        "url": "http://stackstorm.com",
        "feed_updated_at_timestamp": 1426887150
    },
    "entry": {
        "title": "Rackspace::Solve San Francisco",
        "author": "annie",
        "published_at_timestamp": 1425549639,
        "summary": "<p>March 4, 2015 San Francisco, CA Visit StackStorm at Boo [&#8230;]</p>\\n<p>The post <a href=\"http://stackstorm.com/2015/03/05/rackspacesolve/\" rel=\"nofollow\">Rackspace::Solve San Francisco</a> appeared first on <a href=\"http://stackstorm.com\" rel=\"nofollow\">StackStorm</a>.</p>",
        "content": "<p>March 4, 2015<br />\\nSan Francisco, CA<br />\\nVisit StackStorm at Booth #20!</p>\\n<p>During Rackspace::Solve, Rackspace will demonstrate the use of StackStorm to automate autoscaling and continuous integration and delivery pipelines, showing how StackStorm can integrate and then automate heterogeneous environments.</p>\\n<p><img alt=\"Solve\" class=\"alignnone size-medium wp-image-2661\" height=\"48\" src=\"http://stackstorm.com/wp/wp-content/uploads/2015/02/Solve-300x48.jpg\" width=\"300\" /></p>\\n<p><a href=\"http://rackspacesolve.com/sanfrancisco.html\" target=\"_blank\">EVENT WEBSITE</a></p><p>The post <a href=\"http://stackstorm.com/2015/03/05/rackspacesolve/\" rel=\"nofollow\">Rackspace::Solve San Francisco</a> appeared first on <a href=\"http://stackstorm.com\" rel=\"nofollow\">StackStorm</a>.</p>",
        "content_raw": "March 4, 2015\\nSan Francisco, CA\\nVisit StackStorm at Booth #20!\\nDuring Rackspace::Solve, Rackspace will demonstrate the use of StackStorm to automate autoscaling and continuous integration and delivery pipelines, showing how StackStorm can integrate and then automate heterogeneous environments.\\n\\nEVENT WEBSITEThe post Rackspace::Solve San Francisco appeared first on StackStorm."
    }
}
```
