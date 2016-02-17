#Sensu Integration Pack

Integrates with [Sensu](http://sensuapp.org/) monitoring framework.

### Prerequisites
Sensu and StackStorm, up and running. See installation for [Sensu](http://sensuapp.org/docs/latest/guide) and [StackStorm](http://docs.stackstorm.com/install).

## Setup
### Install Sensu pack on StackStorm

1. Install Sensu Pack [StackStorm sensu integration
    pack](https://github.com/StackStorm/st2contrib/tree/master/packs/sensu):

	    st2 run packs.install packs=sensu

	    # Check it:
	    st2 action list --pack=sensu

2. Adjust Sensu API endpoint and credentials in [`/opt/stackstorm/packs/sensu/config.yaml`](./config.yaml) to point to the right Sensu instance.

3. Check that the actions work:

    ```
    st2 run sensu.check_list
    ```

### Configure Sensu to send events to StackStorm

StackStorm Sensu handler `st2_handler.py` is installed on Sensu and sends all **relevant** events to StackStorm. Use Sensu configuration to define **relevant** events.

On StackStorm side, Sensu events will fire a Sensu trigger on each received event. The `sensu.event_handler` trigger type is auto-registered by the handler; you can run the `st2_handler.py` manually to get the trigger created. Once created, you can see the trigger(http://docs.stackstorm.com/rules.html#trigger) with `st2 trigger list --pack=sensu`. It now can be used in StackStorm [Rules](http://docs.stackstorm.com/rules.html) to define what actions to take on which events, based on supplied criteria.

Here are step-by-step instructions:

1. Copy StackStorm Sensu handler and config to Sensu handlers dir:

    ```
    sudo cp /opt/stackstorm/packs/sensu/etc/st2_handler.py /etc/sensu/handlers/st2_handler.py
    sudo cp /opt/stackstorm/packs/sensu/etc/st2_handler.conf /etc/sensu/handlers/st2_handler.conf
    sudo chmod +x /etc/sensu/handlers/st2_handler.py
```
	If Sensu is running on another box, these are the files to get to that box.

2. Set up StackStorm endpoints and credentials in [`st2_handler.conf`](etc/st2_handler.conf).

3. Test the handler manually.

    ```
    cd /etc/sensu/handlers/
    echo '{"client": {"name": 1}, "check":{"name": 2}, "id": "12345"}' | ./st2_handler.py ./st2_handler.conf --verbose
    # You'd see something like the following if the test succeeds.
    Sent sensu event to st2. HTTP_CODE: 202
    ```
4. Note that handler invocation auto-creates Sensu trigger type on StackStorm side. Ensure that the Sensu trigger is created on StackStorm:

    ```
    st2 trigger list --pack=sensu
    ```

5. Create and configure Sensu StackStorm handler - call it `st2` - for sending Sensu events to StackStorm:

    ```json
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

6. Add `st2` handler to `handlers` field of desired sensu checks to route events to StackStorm. Here is how to add st2 handler to Sensu memory check:

    ```json
    cat /etc/sensu/conf.d/check_memory.json
    {
      "checks": {
        "memory": {
          "command": "/etc/sensu/plugins/check-memory.sh -w 128 -c 64",
          "interval": 10,
          "subscribers": [
            "test"
          ],
          "handlers": ["default", "st2"]
        }
      }
    }
    ```
    With this config, the memory events from this check will be sent to StackStorm.

    Refer to [Sensu documentation](http://sensuapp.org/docs/latest/guide) for details on how to configure handlers and checks.

6. Profit. At this point, StackStorm will receive sensu events and fire sensu triggers. Use them in Rules to fire an action, or a workflow of actions, on Sensu event.

### Handler options

1. The handler supports unauthed st2 endpoints (server side authentication turned off). Though
   this is not recommended, you can use this for local testing.

   ```
   echo '{"client": {"name": 1}, "check":{"name": 2}, "id": "12345"}' | ./st2_handler.py ./st2_handler.conf --unauthed
   ```
2. The handler also supports turning on/off ssl verification for all API requests to st2. By
   default, SSL verification is turned off as evaluation versions of st2 ship with self-signed
   certs. To turn on ssl verify, use ```--ssl-verify``` option.

   ```
   echo '{"client": {"name": 1}, "check":{"name": 2}, "id": "12345"}' | ./st2_handler.py ./st2_handler.conf --ssl-verify
   ```

3. If for whatever reason, you've to debug the handler, you can use the --verbose option.

   ```
   echo '{"client": {"name": 1}, "check":{"name": 2}, "id": "12345"}' | ./st2_handler.py ./st2_handler.conf --verbose
   ```

### Example
Let's take monitoring StackStorm itself for end-to-end example. Sensu will watch for StackStorm action runners, `st2actionrunners`, fire an event when it's less then 10. StackStorm will catch the event and trigger an action. A simple action that dumps the event payload to the file will suffice as example; in production the action will be a troubleshooting or remediation workflow.

1. If Sensu `check_procs.rb` check plugin is not yet installed, install it now (look up Sensu [docs here](https://sensuapp.org/docs/0.20/getting-started-with-checks#install-dependencies) for CentOS/RHEL version):

    ```
    sudo apt-get update
    sudo apt-get install ruby ruby-dev
    sudo gem install sensu-plugin

    sudo wget -O /etc/sensu/plugins/check-procs.rb http://sensuapp.org/docs/0.20/files/check-procs.rb
    sudo chmod +x /etc/sensu/plugins/check-procs.rb
    ```

2. Create a Sensu check json like below. This check watches for keeping StackStorm action runners count at 10, and fires an event if the number of runners is less than 10. Note that is using `st2` handler.

    ```json
    cat /etc/sensu/conf.d/check_st2actionrunner.json
    {
      "checks": {
        "st2actionrunner_check": {
          "handlers": ["default", "st2"],
          "command": "/etc/sensu/plugins/check-procs.rb -p st2actionrunner -C 10 ",
          "interval": 60,
          "subscribers": [ "test" ]
        }
      }
    }
    ```
    Make sure the client is configured to get this check via `test` subscription.

    ```json
    cat /etc/sensu/conf.d/client.json
    {
      "client": {
        "name": "test",
        "address": "localhost",
        "subscriptions": [ "test" ]
      }
    }
    ```
    Restart Sensu server and client to pick up the changes:

    ```
    sudo service sensu-server restart
    sudo service sensu-client restart
    ```
    At this point sensu should be

3. Now back to StackStorm. Create StackStorm rule definition (This sample is a part of the pack, [`rules/sample.on_action_runner_check.yaml`](rules/sample.on_action_runner_check.yaml)):

    ```yaml
    cat /opt/stackstorm/packs/sensu/rules/sample.on_action_runner_check
    ---
      name: sample.on_actoin_runner_check
      description: Sample rule that dogfoods st2.
      pack: sensu
      trigger:
        type: sensu.event_handler
      criteria:
        trigger.check.name:
          pattern: "st2actionrunner_check"
          type: "equals"
        trigger.check.output:
          pattern: "CheckProcs CRITICAL*"
          type: "matchregex"
      action:
        ref: "core.local"
        parameters:
          cmd: "echo \"{{trigger}}\" >> /tmp/sensu-sample.out"
      enabled: true
    ```

    and load the rule:

    ```
    cd /opt/stackstorm/packs/sensu
    st2 rule create rules/sample.on_action_runner_check.yaml
    ```
    StackStorm is now waiting for Sensu event.

4. Fire it up: create a Sensu event by Killing an st2actionrunner process.

    ```
    ps auxww | grep st2actionrunner
    sudo kill <pick any pid from the output above>
    ```
    Wait for sensu event to be triggered - check [Uchiwa](https://github.com/sensu/uchiwa) if you have it, or watch the log:
    ```
    tail -f /var/log/sensu/sensu-server.log | grep --line-buffered st2actionrunner
    ```

    Watch the action triggered in StackStorm: `st2 execution list`.  and verify the result by ckecking the file created by the action:

    ```
    cat /tmp/sensu-sample.out
    {'client': {'timestamp': 1440745086, 'version': '0.20.3', 'name': 'test', 'address':
     'localhost', 'subscriptions': ['test']}, 'occurrences': 17, 'action': 'create',
     'timestamp': 1440745095, 'check': {'status': 2, 'executed': 1440745095,
     'total_state_change': 4, 'handlers': ['default', 'st2'], 'issued': 1440745095,
     'interval': 60, 'command': '/etc/sensu/plugins/check-procs.rb -p st2actionrunner
     -C 10 ', 'subscribers': ['test'], 'duration': 0.057, 'output': 'CheckProcs CRITICAL:
     Found 8 matching processes; cmd /st2actionrunner/\n', 'history': ['0', '0', '0',
     '0', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2',
     '2'], 'name': 'st2actionrunner_check'}, 'id':'a1723d77-6afe-4555-8bae-7a8423e8a26d'}
    ...
    ```

    You can also see that the rule triggered an action in StackStorm UI, under History tab.

5. In this simple example, StackStorm just dumped the content of the check output to the file. In a real auto-remediation, a workflow of actions will get StackStorm runners back to normal. For now, just do that manually:

    ```
    st2ctl restart
    ```

Enjoy StackStorm with Sensu!

