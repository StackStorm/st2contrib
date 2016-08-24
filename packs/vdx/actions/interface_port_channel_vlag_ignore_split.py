from pynos import device
from st2actions.runners.pythonrunner import Action


class interface_port_channel_vlag_ignore_split(Action):
    def run(self, **kwargs):
        conn = (str(kwargs.pop('ip')), str(kwargs.pop('port')))
        auth = (str(kwargs.pop('username')), str(kwargs.pop('password')))
        test = kwargs.pop('test', False)
        callback = kwargs.pop('callback', None)
        with device.Device(
            conn=conn, auth=auth,
            test=test,
            callback=callback
        ) as dev:
            dev.interface.port_channel_vlag_ignore_split(**kwargs)
        return 0
