from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionGetAction'
]


class St2ExecutionGetAction(St2BaseAction):
    def run(self, id):
        result = self._run_client_method(method=self.client.liveactions.get_by_id,
                                         method_kwargs={'id': id},
                                         format_func=lambda x: x.to_dict())
        return result
