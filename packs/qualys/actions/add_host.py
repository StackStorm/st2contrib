from lib.base import QualysBaseAction

__all__ = [
    'AddHostAction'
]


class AddHostAction(QualysBaseAction):
    def run(self, host, vulnerability_management, policy_compliance):
        if policy_compliance and vulnerability_management:
            host_type = 'both'
        elif policy_compliance and not vulnerability_management:
            host_type = 'pc'
        elif not policy_compliance and vulnerability_management:
            host_type = 'vm'
        else:
            host_type = ''
        host = self.connection.addHost(host, host_type)
        return self.resultsets.formatter(host)
