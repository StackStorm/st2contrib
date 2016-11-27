from lib.sensu import SensuAction

__all__ = [
    'CheckRequestAction'
]


class CheckRequestAction(SensuAction):
    def run(self, check, subscribers):
        return self.api.post_check_request(check, subscribers)
