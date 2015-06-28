from lib.mmonit import MmonitBaseAction


class MmonitDismissEvent(MmonitBaseAction):
    def run(self, event_id):
        self.login()
        data = {"id": event_id}
        self.session.post("{}/reports/events/dismiss".format(self.url), data=data)
        self.logout()
        return True
