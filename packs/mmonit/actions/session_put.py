from lib.mmonit import MmonitBaseAction


class MmonitSessionPut(MmonitBaseAction):
    def run(self, attribute):
        # Try to protect against wrongly input and fail fast if so
        try:
            k, v = attribute.split(":")
        except:
            error = ("The key/value pair {} don't seem to follow the key:value format".format(
                     attribute))
            raise Exception(error)
        data = {k: v}

        self.login()
        self.session.post("{}/session/put".format(self.url), data=data)
        self.logout()
        return True
