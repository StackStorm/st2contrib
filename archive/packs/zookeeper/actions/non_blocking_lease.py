from datetime import timedelta
from socket import gethostname
import sys
from uuid import uuid4

from kazoo.client import KazooClient

from st2actions.runners.pythonrunner import Action


class NonBlockingLease(Action):
    """
    Exclusive lease that does not block.

    An exclusive lease ensures that only one client at a time owns the lease.
    The action exits successfully if the lease was obtained and with code 1 otherwise.

    A common use case is a situation where a task should only run on a single host.  In this case,
    the clients that did not obtain the lease should exit without performing the protected task.

    The lease stores time stamps using client clocks, and will therefore only work if client clocks
    are roughly synchronised.  It uses UTC, and works across time zones and daylight savings.
    """

    # NOTE: the drift on the clocks running cronjobs controlled by this lease must be
    # less than the frequency - the lease_time. For example, a cronjob running every
    # minute with a lease_time of 30s means that your clocks must all be within 30s of
    # each other or nobody will ever get the lease.
    #
    # Changing the threshold allows you to decide whether it's more important that
    # the job always runs (and sometimes twice) or if it's better to run only once
    # or not at all. With a lease_time of 50, if clocks drift by more than 10s, it
    # will appear as though the lease is always taken and your job will never run.
    # (Conversely, with a lease_time of 10 and a drift of >10s, two hosts will both
    # get a lease, running your job twice.)

    def __init__(self, config):
        super(NonBlockingLease, self).__init__(config)
        self.hosts = self.config['zookeeper_hosts']
        self.root = self.config['zookeeper_root']

    def run(self, lease_name, lease_time):
        zk = KazooClient(hosts=self.hosts)
        zk.start()
        path = "%s/%s" % (self.root, lease_name)
        # unique id ensures only one action execution if multiple executions on the same host
        identifier = '%s: %s' % (gethostname(), uuid4())
        duration = timedelta(seconds=lease_time)
        lease = zk.NonBlockingLease(path, duration, identifier=identifier)
        if not lease:
            sys.exit(1)
