from lib.mmonit import MmonitBaseAction


class MmonitGetEvent(MmonitBaseAction):
    def run(self, event_id):
        self.login()
        data = {"id": event_id}
        req = self.session.get("{}/reports/events/get".format(self.url), params=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
