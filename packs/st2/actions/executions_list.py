from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionsListAction'
]


class St2ExecutionsListAction(St2BaseAction):
    def run(self, action=None, status=None):
        kwargs = {}

        if action:
            kwargs['action'] = action

        if status:
            kwargs['status'] = status

        result = self.client.liveactions.query(**kwargs)
        return result
