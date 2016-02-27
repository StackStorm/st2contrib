from lib.base import QualysBaseAction

__all__ = [
    'LaunchScanAction'
]


class LaunchScanAction(QualysBaseAction):
    def run(self, title, option_title, iscanner_name,
            asset_groups=None, ip=None):
        scan = self.connection.launchScan(title, option_title,
                                          iscanner_name, asset_groups, ip)
        return self.resultsets.formatter(scan)
