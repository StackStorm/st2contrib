from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionsReRunAction'
]


def format_result(item):
    if not item:
        return None

    return item.to_dict()


class St2ExecutionsReRunAction(St2BaseAction):
    def run(self, id, parameters=None):
        parameters = parameters or {}
        result = self.client.liveactions.re_run(execution_id=id,
                                                parameters=parameters)
        result = format_result(item=result)
        return result
