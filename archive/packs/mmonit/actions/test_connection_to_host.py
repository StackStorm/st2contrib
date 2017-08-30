from lib.mmonit import MmonitBaseAction


class MmonitTestConnectionHost(MmonitBaseAction):
    def run(self, ipaddr, ssl, port, monituser, monitpassword):
        self.login()
        data = {"ipaddr": ipaddr, "port": port, "ssl": ssl, "monituser": monituser,
                "monitpassword": monitpassword}
        req = self.session.post("{}/admin/hosts/test".format(self.url), data=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
