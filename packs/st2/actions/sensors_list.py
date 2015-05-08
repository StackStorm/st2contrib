from lib.action import St2BaseAction

__all__ = [
    'St2SensorsListAction'
]


class St2SensorsListAction(St2BaseAction):
    def run(self, pack=None):
        kwargs = {}

        if pack:
            kwargs['pack'] = pack

        result = self.client.sensors.get_all(**kwargs)
        return result
