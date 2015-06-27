from lib.mmonit import MmonitBaseAction


class MmonitSummaryEvents(MmonitBaseAction):
    def run(self):
        self.login()
        req = self.session.get("{}/reports/events/summary".format(self.url))

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
