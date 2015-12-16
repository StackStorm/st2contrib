# Date / time integration pack

Pack containing various actions for working with dates and times.

## Actions

### get_week_boundaries

Retrieve week boundaries for the provided date as `(week_start_date_ts,
week_end_date_ts)` tuple.

### parse_date_string

Action which parses the provided date string and returns a timestamp. Keep in
mind that this function supports many different dates formats (including human
friendly ones) such as:

* `1 hour ago`
* `10 days ago`
* `12/12/12`
* `2015-12-10`
* `13 января 2015 г. в 13:34`
* etc.
