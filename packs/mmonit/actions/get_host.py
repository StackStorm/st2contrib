from lib.mmonit import MmonitBaseAction


class MmonitGetHost(MmonitBaseAction):
    def run(self, host_id):
        self.login()
        data = {"id": host_id}
        req = self.session.get("{}/admin/hosts/get".format(self.url), params=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
