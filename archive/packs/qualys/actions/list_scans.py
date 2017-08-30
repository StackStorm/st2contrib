from lib.base import QualysBaseAction

__all__ = [
    'ListScansAction'
]


class ListScansAction(QualysBaseAction):
    def run(self, launched_after="", state="", target="",
            scan_type="", user_login=""):
        scans = self.connection.listScans(launched_after, state,
                                          target, scan_type, user_login)
        return self.resultsets.formatter(scans)
