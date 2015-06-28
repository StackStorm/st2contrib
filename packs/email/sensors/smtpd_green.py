from eventlet import patcher
from eventlet.green import socket
from eventlet.green import time
from eventlet.green import asyncore
from eventlet.green import asynchat


patcher.inject(
    "smtpd",
    globals(),
    ('socket', socket),
    ('asyncore', asyncore),
    ('asynchat', asynchat),
    ('time', time))

del patcher
