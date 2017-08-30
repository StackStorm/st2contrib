from lib.mmonit import MmonitBaseAction


class MmonitActionHost(MmonitBaseAction):
    def run(self, host_id, action, service):
        self.login()
        data = {"service": service, "id": host_id, "action": action}
        self.session.post("{}/admin/hosts/action".format(self.url), data=data)
        self.logout()
        return True
