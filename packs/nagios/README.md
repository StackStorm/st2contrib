## Nagios integration

To integrate Nagios with st2, we will need to add a nagios event handler which POSTs a HTTP webbhook to st2.

## Nagios event handler

The event handler script is available at [etc/st2service_handler.py](etc/st2service_handler.py).

## Configuring the event handler

The event handler tries to register a trigger type first before sending any
notifications to st2. This trigger type is then referenced in st2 rules. See
[rules/](rules/) for examples.

## Installing the event handler

1. Pick the nagios host where you want the event handler to be placed.
2. Copy st2service_handler.py  and st2service_handler.yaml to /usr/local/nagios/libexec/

    ```bash
    cp st2service_handler.* /usr/local/nagios/libexec/
    ```
3. Make sure st2service_handler.py is executable.

    ```bash
    chmod +x /usr/local/nagios/libexec/st2service_handler.py
    ```
4. Handlers require a configuration file (See [etc/st2service_handler.yaml](etc/st2service_handler.yaml)) containing
   st2 credentials, st2 API URL and st2 auth URL, st2 API Key, Unauthed and SSL Verify Flag.

5. Test the event handler manually.

    ```bash
    python st2service_handler.py st2service_handler.yaml 44534 3 WARNING HARD "/var/log" 4 host-name
    # You'd see something like the following if the test succeeds.
    Sent nagios event to st2. HTTP_CODE: 202
    ```

## Handler options

1. The handler supports unauthed st2 endpoints (server side authentication turned off). Though
   this is not recommended, you can use this for local testing. To turn on the unauthed flag to
   true in st2service_handler.yaml

   ```
   unauthed: True
   ```
2. The handler also supports turning on/off ssl verification for all API requests to st2. By
   default, SSL verification is turned off as evaluation versions of st2 ship with self-signed
   certs. To turn on ssl verify, change the flag in st2service_handler.yaml to `True`.

   ```
   ssl_verify: True
   ```
3. If for whatever reason, you've to debug the handler, you can use the --verbose option.

   ```bash
   python st2service_handler.py st2service_handler.yaml 44534 3 WARNING HARD "/var/log" 4 host-name --verbose
   ```
