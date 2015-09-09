from lib.mmonit import MmonitBaseAction


class MmonitSummaryStatus(MmonitBaseAction):
    def run(self):
        self.login()
        req = self.session.get("{}/admin/hosts/summary".format(self.url))

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
