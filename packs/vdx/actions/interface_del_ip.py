from pynos import device
from st2actions.runners.pythonrunner import Action


class interface_del_ip(Action):
    def run(self, **kwargs):
        conn = (str(kwargs.pop('ip')), str(kwargs.pop('port')))
        auth = (str(kwargs.pop('username')), str(kwargs.pop('password')))
        with device.Device(conn=conn, auth=auth) as dev:
            dev.interface.del_ip(**kwargs)
        return 0
