from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionGetAction'
]


def format_result(item, exclude_attributes):
    if not item:
        return None

    return item.to_dict(exclude_attributes=exclude_attributes)


class St2ExecutionGetAction(St2BaseAction):
    def run(self, id, exclude):
        result = self._run_client_method(method=self.client.liveactions.get_by_id,
                                         method_kwargs={'id': id},
                                         format_func=format_result,
                                         format_kwargs={
                                             'exclude_attributes': exclude
                                         })
        return result
