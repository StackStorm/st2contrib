from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionGetAction'
]

EXCLUDE_ATTRIBUTES = [
    'trigger',
    'trigger_type',
    'trigger_instance',
    'liveaction',
    'context'
]


def format_result(item):
    if not item:
        return None

    return item.to_dict(exclude_attributes=EXCLUDE_ATTRIBUTES)


class St2ExecutionGetAction(St2BaseAction):
    def run(self, id):
        result = self._run_client_method(method=self.client.liveactions.get_by_id,
                                         method_kwargs={'id': id},
                                         format_func=format_result)
        return result
