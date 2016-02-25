#!/usr/bin/env python2.7

import argparse
import socket
import time


def wait_net_service(server, port, sleep=10, timeout=5):
    """ Wait for network service to appear
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """

    s = socket.socket()

    while True:
        try:
            s.settimeout(timeout)
            s.connect((server, port))
        except:
            time.sleep(sleep)
        else:
            s.close()
            return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port open checker.')
    parser.add_argument('--server', '--h', required=True,
                        help='Server address.'),
    parser.add_argument('--check_port', '-p', required=True, type=int,
                        help='Port to check.')
    parser.add_argument('--timeout', '-t', required=False, type=float,
                        help='Socket timeout.', default=5)
    parser.add_argument('--sleep', '-s', required=False, type=float,
                        help='Sleep on socket timeout', default=10)
    args = parser.parse_args()

    wait_net_service(args.server, args.check_port,
                     sleep=args.sleep,
                     timeout=args.timeout)
