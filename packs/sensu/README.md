#Sensu Integration Pack

Integrates with beautiful [Sensu](http://sensuapp.org/) monitoring framework.

### Prerequisites
A box with Sensu and StackStorm up and running. See installation for [Sensu](http://sensuapp.org/docs/latest/guide) and [StackStorm](http://docs.stackstorm.com/install).


## How it works

#### Triggers

StackStorm Sensu handler `st2_handler.py` is installed on Sensu and sends all **relevant** events to StackStorm. Use Sensu configuration to define what **relevant**.

On StackStorm side, sensu events will fire a sensu trigger on each received event. The `sensu.event_handler` trigger type is auto-registered by the handler; you can run the `st2_handler.py` manually to get the trigger created. Once created, you can see the trigger(http://docs.stackstorm.com/rules.html#trigger) with `st2 trigger list --pack=sensu`. It now can be is used in StackStorm [Rules](http://docs.stackstorm.com/rules.html) to define what actions to take on which events, based on supplied criteria.

### Actions
Actions work as usual. See [`./actions`](./actions) for what is available.

## Setup
### Install Sensu pack on StackStorm

1. Install Sensu Pack [StackStorm sensu integration
    pack](https://github.com/StackStorm/st2contrib/tree/master/packs/sensu):

	    st2 run packs.install packs=sensu

	    # Check it:
	    st2 action list -pack=sensu

1. Adjust Sensu API endpoint and credentials in [`/opt/stackstorm/packs/sensu/config.yaml`](./config.yaml) to point to the right Sensu instance.

1. Check that the actions work:

    ```
    st2 run sensu.check_list
    ```

### Configure Sensu to send events to StackStorm
1. Copy StackStorm Sensu handler and config to Sensu handlers dir:

    ```
    sudo cp /opt/stackstorm/packs/sensu/etc/st2_handler.py /etc/sensu/handlers/st2_handler.py
    sudo cp /opt/stackstorm/packs/sensu/etc/st2_handler.conf /etc/sensu/handlers/st2_handler.conf
    sudo chmod +x /etc/sensu/handlers/st2_handler.py
```
	If Sensu is running on another box, these are the files to get to that box.

2. Set up StackStorm endpoints and credentials in [`st2_handler.conf`](etc/st2_handler.conf).

3. Test the handler manually. Note that it

    ```
    $ echo '{"foo":"bar"}' | ./st2_handler.py st2_handler.conf
    Registered trigger type with st2.
    POST: url: http://localhost:9101/webhooks/st2/, body: {'trigger': 'sensu.event_handler', 'payload': {'foo': 'bar'}}
    Sent sensu event to st2. HTTP_CODE: 202
    ```
3. Create and configure Sensu handler for sending Sensu events to StackStorm:

    ```
    cat /etc/sensu/conf.d/handler_st2.json
    {
        "handlers": {
            "st2": {
              "type": "pipe",
              "command": "/etc/sensu/handlers/st2_handler.py /etc/sensu/handlers/st2_handler.conf"
            }
        }
    }
    ```

4. Refer the `st2` handler in Sensu checks `handler` field to route events to StackStorm. Example:

    ```
    cat /etc/sensu/conf.d/check_st2actionrunner.json
    {
      "checks": {
        "cron_check": {
          "handlers": ["default", "st2"],
          "command": "/etc/sensu/plugins/check-procs.rb -p st2actionrunner -C 10 ",
          "interval": 60,
          "subscribers": [ "webservers" ]
        }
      }
    }
    ```

    Refer to [Sensu documentation](http://sensuapp.org/docs/latest/guide) for guidance.

### Handy hints
* To remove `sensu.event_handler` from StackStorm:

        http DELETE http://localhost:9101/v1/triggertypes/sensu.event_handler x-auth-token:`echo $ST2_AUTH_TOKEN`
