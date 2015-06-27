from lib.mmonit import MmonitBaseAction


class MmonitDeleteHost(MmonitBaseAction):
    def run(self, host_id):
        self.login()
        data = {"id": host_id}
        self.session.post("{}/admin/hosts/delete".format(self.url), data=data)
        self.logout()
        return True
