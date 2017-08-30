from lib.base import QualysBaseAction

__all__ = [
    'ListHostsNotScannedSinceAction'
]


class ListHostsNotScannedSinceAction(QualysBaseAction):
    def run(self, days):
        hosts = self.connection.notScannedSince(days)
        return self.resultsets.formatter(hosts)
