from lib.mmonit import MmonitBaseAction


class MmonitListHosts(MmonitBaseAction):
    def run(self, host_id):
        self.login()
        req = self.session.get("{}/admin/hosts/list".format(self.url))

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
