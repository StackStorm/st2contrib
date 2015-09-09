## Nagios integration

To integrate Nagios with st2, we will need to add a nagios event handler which POSTs a HTTP webbhook to st2.

## Nagios event handler

The event handler script is available in [etc/st2service_handler.py](etc/st2service_handler.py).

## Configuring the event handler

The event handler tries to register a trigger type first before sending any
notifications to st2. This trigger type is then referenced in st2 rules. See
[rules/](rules/) for examples.

## Installing the event handler

1. Pick the nagios host where you want the event handler to be placed.
2. Copy st2service_handler.py to /usr/local/nagios/libexec/

    ```
    cp st2service_handler.py /usr/local/nagios/libexec/
    ```
3. Make sure st2service_handler.py is executable.

    ```
    chmod +x /usr/local/nagios/libexec/st2service_handler.py
    ```
4. Handlers require a configuration file (See [etc/config.yaml](etc/config.yaml)) containing
st2 credentials, st2 API URL and st2 auth URL.





