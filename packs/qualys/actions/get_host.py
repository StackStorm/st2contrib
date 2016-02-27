from lib.base import QualysBaseAction

__all__ = [
    'GetHostAction'
]


class GetHostAction(QualysBaseAction):
    def run(self, host):
        host = self.connection.getHost(host)
        return self.resultsets.formatter(host)
