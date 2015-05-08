from lib.action import St2BaseAction

__all__ = [
    'St2RulesListAction'
]


class St2RulesListAction(St2BaseAction):
    def run(self, pack=None):
        kwargs = {}

        if pack:
            kwargs['pack'] = pack

        result = self.client.rules.get_all(**kwargs)
        return result
