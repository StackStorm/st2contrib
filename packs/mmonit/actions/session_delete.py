from lib.mmonit import MmonitBaseAction


class MmonitSessionDelete(MmonitBaseAction):
    def run(self, session_key=""):
        self.login()
        data = {"key": session_key}
        self.session.post("{}/session/delete".format(self.url), data=data)
        self.logout()
        return True
