from lib.mmonit import MmonitBaseAction


class MmonitSessionGet(MmonitBaseAction):
    def run(self, session_key=""):
        self.login()
        data = {"key": session_key}
        req = self.session.post("{}/session/get".format(self.url), data=data)
        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
