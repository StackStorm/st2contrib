from lib.action import St2BaseAction

__all__ = [
    'St2ActionsListAction'
]


class St2ActionsListAction(St2BaseAction):
    def run(self, pack=None):
        kwargs = {}

        if pack:
            kwargs['pack'] = pack

        result = self.client.actions.get_all(**kwargs)
        return result
