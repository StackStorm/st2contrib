from pynos import device
from st2actions.runners.pythonrunner import Action

class bgp_neighbor(Action):
    def run(self, **kwargs):
        conn = (str(kwargs.pop('ip')), str(kwargs.pop('port')))
        auth = (str(kwargs.pop('username')), str(kwargs.pop('password')))
        with device.Device(conn=conn, auth=auth) as dev:
            dev.bgp.neighbor(**kwargs)
        return 0