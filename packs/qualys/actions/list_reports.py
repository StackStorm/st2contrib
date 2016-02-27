from lib.base import QualysBaseAction

__all__ = [
    'ListReportsAction'
]


class ListReportsAction(QualysBaseAction):
    def run(self):
        reports = self.connection.listReports()
        return self.resultsets.formatter(reports)
