# Splunk Integration Pack

Basic integration with Splunk Enterprise, Splunk Cloud, or Splunk Light: http://www.splunk.com/en_us/products.html

## Configuration

Copy the example configuration in [splunk.yaml.example](./splunk.yaml.example)
to `/opt/stackstorm/configs/splunk.yaml` and edit as required.

It should contain:

* ``host`` - Splunk server
* ``port`` - Splunk API port (default 8089)
* ``username`` - Splunk username
* ``password`` - Splunk password

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions

### search

Runs a synchronous search to get Splunk data. E.g., `st2 run splunk.search query='search * | head 10`. Refer to [Splunk documentation](http://docs.splunk.com/Documentation/Splunk/5.0/Search/Aboutthesearchlanguage) for search query syntax.

## Sensors

TBD
