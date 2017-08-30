[![Check_MK](./logo.png)](https://mathias-kettner.com/check_mk.html)

# Check_MK Integration Pack

Integrates with [Check_MK](https://mathias-kettner.com/check_mk.html) monitoring framework.

## Configuration

### Install Check_MK pack on StackStorm

Install the [StackStorm Check_MK integration pack](https://github.com/StackStorm/st2contrib/tree/master/packs/check_mk):

        st2 run packs.install packs=check_mk

### Configure Check_MK to send events to StackStorm

StackStorm Check_MK handler `stackstorm.py` is installed and sends all **relevant** events to
StackStorm. Use Check_MK to define **relevant** events.

On StackStorm side, Check_MK events will fire a Check_MK trigger on each received event. You must
manually register the `check_mk.event_handler` trigger type during setup. It can now be used in
StackStorm [Rules](http://docs.stackstorm.com/rules.html) to define what actions to take on which
events, based on supplied criteria.

Here are step-by-step instructions:

1. Register StackStorm Check_MK trigger:

        st2 trigger create /opt/stackstorm/packs/check_mk/triggers/event_handler.yaml

    If you're using StackStorm v1.5+ this will be automatically registered like actions, sensors, etc.

2. Copy StackStorm Check_MK handler and config to Check_MK directories:

        cd /opt/stackstorm/packs/check_mk/
        sudo cp etc/stackstorm.conf /etc/check_mk/stackstorm.conf
        # Your local Check_MK installation path might differ
        sudo cp etc/stackstorm.py /omd/sites/<master>/local/share/check_mk/notifications/stackstorm.py
        sudo chmod +x /omd/sites/<master>/local/share/check_mk/notifications/stackstorm.py

    If Check_MK is running on another box, these are the files to get to that box. If running
    replicated Check_MK, these must be placed on your master Check_MK node/site. You must adjust
    the path to your local Check_MK installation appropriately. Example is shown with OMD-based
    install using a master node/site creatively named `master`.

3. Set up StackStorm endpoints and credentials in [`stackstorm.conf`](etc/stackstorm.conf).

4. Install the StackStorm handler dependencies on the Check_MK master node:

        pip install -r /opt/stackstorm/packs/check_mk/requirements.txt

5. Test the handler manually.

        cd /omd/sites/<master>/local/share/check_mk/notifications/
        # Check_MK passes data to notification scripts via environment variables
        source /opt/stackstorm/packs/check_mk/etc/sample_event.sh
        ./stackstorm.py
        # You'd see something like the following if the test succeeds
        Sent event to StackStorm. HTTP_CODE: 200. TRACE_TAG: a27b817e-f24d-4d24-be75-dcb8a47204d0

6. Create and configure Check_MK StackStorm handler for sending Check_MK events to StackStorm.

    1. **Notifications**: WATO users navigate to Notifications.
    2. **New Rule**: Create a global notification rule by clicking "New Rule".
    3. **Notification Method**: Select "StackStorm" from the Notification Method dropdown.
    4. **Contact Selection**: Choose any contact. Each event will be once per contact to StackStorm,
       so only choose one.
    5. **Conditions**: Apply conditions as you like or leave as-is to send all events to StackStorm.

   You can alternatively send select events to StackStorm using the Flexible Notification System.

   Refer to the [Check_MK documentation](http://mathias-kettner.com/cms.html) for details on how
   to configure notifications.

7. Profit. At this point, StackStorm will receive Check_MK events and fire Check_MK triggers.
   Use them in Rules to fire an action, or a workflow of actions, on Check_MK event.

Enjoy StackStorm with Check_MK!

## Triggers

Trigger            | Description
------------------ | ---------------------------------------------
**event_handler**  | Fired when an event is received from Check_MK

## Sample Check_MK Payload

Here's a sample payload with all the data sent by the StackStorm handler. This example shows
a root filesystem (`fs_/`) check on localhost going from OK to CRITICAL.

    {
      "notification_type": "PROBLEM",
      "timestamp": 1352405221,
      "parameters": [
        "0199399485",
        "Foo/Bar"
      ],
      "contact": {
        "name": "hirni",
        "email": "mk@hirni.de",
        "pager": ""
      },
      "host": {
        "name": "localhost",
        "alias": "localhost",
        "address": "127.0.0.1",
        "state": "UP",
        "last_state": "UP",
        "output": "OK - 127.0.0.1: rta 0.054ms, lost 0%",
        "perf_data": "rta=0.054ms;200.000;500.000;0; pl=0%;40;80;;",
        "check_command": "check-mk-ping",
        "notification_number": "0",
        "long_output": ""
      },
      "service": {
        "desc": "fs_/",
        "state": "CRITICAL",
        "last_state": "OK",
        "output": "CRIT - 90.0% used (18.27 of 20.3 GB)",
        "perf_data": "/=18712.1132812MB;16630;18709;0;20788.5820",
        "check_command": "check_mk-df",
        "notification_number": "7",
        "long_output": ""
      }
    }
