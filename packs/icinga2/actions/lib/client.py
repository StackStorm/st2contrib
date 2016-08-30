# pylint: disable=no-member
import json
import urllib
import signal
import sys
import time
import pycurl

POST_PARAMS = {}
MAX_ATTEMPTS = 3


class Client:
    def __init__(self, action, api_url, api_user, api_password, method):
        self.conn = None
        self.action = action
        self.keep_trying = 1
        self.api_url = api_url
        self.api_user = api_user
        self.api_password = api_password
        self.method = method
        self.buffer = ''
        signal.signal(signal.SIGINT, self.handle_ctrl_c)

    def handle_ctrl_c(self, signal, frame):
        sys.stderr.write('SIGINT receivied')
        sys.stderr.write('You pressed Ctrl+C?!')
        self.abort_session()

    def abort_session(self):
        self.keep_trying = 0
        self.conn.close()

    def setup_connection(self):

        if self.conn:
            self.conn.close()
        self.headers = ['Accept: application/json', 'Expect:', 'Connection: close']
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.SSL_VERIFYHOST, False)
        self.conn.setopt(pycurl.SSL_VERIFYPEER, False)
        self.conn.setopt(pycurl.USERPWD, "%s:%s" % (self.api_user, self.api_password))
        self.conn.setopt(pycurl.URL, self.api_url)
        self.conn.setopt(pycurl.VERBOSE, 0)
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
        self.conn.setopt(pycurl.NOSIGNAL, 1)
        self.conn.setopt(pycurl.NOPROGRESS, 1)
        self.conn.setopt(pycurl.HTTPHEADER, self.headers)
        if self.method == 'post':
            self.conn.setopt(pycurl.POST, 1)
            self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        elif self.method == 'get':
            self.conn.setopt(pycurl.POST, 0)

    def on_receive(self, data):
        # self.action.logger.debug('Icinga2GetStatus: client on_receive, data: %s', data)
        # complete message received
        self.buffer += data
        # sys.stderr.write(data)
        try:
            event = json.loads(self.buffer)
            update_body = True
        except:
            # no json found
            update_body = False

        if update_body:
            if self.action is not None:
                # sys.stderr.write('Updating body\n')
                self.action.set_body(event)
            else:
                print event

    def __del__(self):
        self.conn.close()

    def make_call(self):
        backoff_network_error = 0.25
        backoff_http_error = 1
        backoff_rate_limit = 60
        attempt = 0
        while True and self.keep_trying == 1 and attempt < MAX_ATTEMPTS:
            attempt += 1
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                if self.keep_trying == 0:
                    continue
                sys.stderr.write('Network error: %s' % self.conn.errstr())
                sys.stderr.write('Waiting %s seconds before trying again' % backoff_network_error)
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 200:
                # sys.stderr.write('HTTP request successful.')
                self.conn.close()
                break
            elif sc == 420:
                # Rate limit, use exponential back off starting with 1 minute then doubling
                sys.stderr.write('Rate limit, waiting %s seconds' % backoff_rate_limit)
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            elif sc == 401:
                # Authentication error
                sys.stderr.write('Authentication error, check user/password.')
                self.action.error = 1
                break
            elif sc == 404:
                # Authorization error
                sys.stderr.write('Object not found. Verify request and/or check permissions.')
                self.action.error = 2
                break
            elif sc == 400:
                # Authorization error
                sys.stderr.write('Bad request.')
                self.action.error = 3
                break
            else:
                # HTTP error, use exponential back off up to 320 seconds
                sys.stderr.write('HTTP error %s, %s' % (sc, self.conn.errstr()))
                sys.stderr.write('Waiting %s seconds' % backoff_http_error)
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 10)
