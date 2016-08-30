# pylint: disable=no-member
import json
import urllib
import signal
import time
import pycurl

POST_PARAMS = {}


class Client:
    def __init__(self, sensor, api_url, api_user, api_password):
        if sensor is not None:
            self._sensor = sensor
        else:
            self._sensor = None
        self.conn = None
        self.buffer = ''
        self.keep_trying = 1
        self.api_url = api_url
        self.api_user = api_user
        self.api_password = api_password

        signal.signal(signal.SIGINT, self.handle_ctrl_c)

    def handle_ctrl_c(self, signal, frame):
        if self._sensor is not None:
            self._sensor.logger.info('SIGINT receivied')
        else:
            print 'You pressed Ctrl+C!'
        self.abort_session()

    def abort_session(self):
        self.keep_trying = 0
        self.conn.close()

    def setup_connection(self):

        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.headers = ['Accept: application/json', 'Expect:']
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.SSL_VERIFYHOST, False)
        self.conn.setopt(pycurl.SSL_VERIFYPEER, False)
        self.conn.setopt(pycurl.USERPWD, "%s:%s" % (self.api_user, self.api_password))
        self.conn.setopt(pycurl.URL, self.api_url)
        self.conn.setopt(pycurl.VERBOSE, 1)
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
        self.conn.setopt(pycurl.NOSIGNAL, 1)
        self.conn.setopt(pycurl.NOPROGRESS, 0)
        self.conn.setopt(pycurl.PROGRESSFUNCTION, self.on_progress)
        self.conn.setopt(pycurl.HTTPHEADER, self.headers)
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))

    def on_receive(self, data):
        self.buffer += data
        if data.endswith('\n') and self.buffer.strip():
            # complete message received
            event = json.loads(self.buffer)
            self.buffer = ''
            if self._sensor is not None:
                self._sensor.process_event(event)
            else:
                print event

    def on_progress(self, d_total, downloaded, u_total, uploaded):
        pass
        # print "on_progress called"

    def __del__(self):
        self.conn.close()

    def start(self):
        if self._sensor is not None:
            self._sensor.logger.info('pyCurl started.')
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True and self.keep_trying == 1:
            if self._sensor is not None:
                self._sensor.logger.info('keep trying = %i', self.keep_trying)
            else:
                print "keep trying = %i" % self.keep_trying
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                if self.keep_trying == 0:
                    continue
                if self._sensor is not None:
                    self._sensor.logger.info('Network error: %s', self.conn.errstr())
                    self._sensor.logger.info('Waiting %s seconds before trying again',
                                             backoff_network_error)
                else:
                    print 'Network error: %s' % self.conn.errstr()
                    print 'Waiting %s seconds before trying again' % backoff_network_error
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute, and doubling
                if self._sensor is not None:
                    self._sensor.logger.info('Rate limit, waiting %s seconds', backoff_rate_limit)
                else:
                    print 'Rate limit, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            elif sc == 401:
                # Authentication error
                if self._sensor is not None:
                    self._sensor.logger.info(
                        'Authentication error, check user/password, waiting %s seconds',
                        backoff_rate_limit)
                else:
                    print 'Authentication error, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            elif sc == 404:
                # Authorization error
                if self._sensor is not None:
                    self._sensor.logger.info(
                        'Authorization error, check permissions, waiting %s seconds',
                        backoff_rate_limit)
                else:
                    print 'Authorization error, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                if self._sensor is not None:
                    self._sensor.logger.info('HTTP error %s, %s', sc, self.conn.errstr())
                    self._sensor.logger.info('Waiting %s seconds', backoff_http_error)
                else:
                    print 'HTTP error %s, %s' % (sc, self.conn.errstr())
                    print 'Waiting %s seconds' % backoff_http_error
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)
