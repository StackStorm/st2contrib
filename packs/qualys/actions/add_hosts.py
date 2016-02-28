from lib.base import QualysBaseAction

__all__ = [
    'AddHostsAction'
]


class AddHostsAction(QualysBaseAction):
    def run(self, hosts, vulnerability_management, policy_compliance):
        if policy_compliance and vulnerability_management:
            host_type = 'both'
        elif policy_compliance and not vulnerability_management:
            host_type = 'pc'
        elif not policy_compliance and vulnerability_management:
            host_type = 'vm'
        else:
            host_type = ''
        hosts = self.connection.addHost(str.join(',', hosts), host_type)
        return self.resultsets.formatter(hosts)
