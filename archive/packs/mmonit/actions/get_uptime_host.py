from lib.mmonit import MmonitBaseAction


class MmonitGetUptimeHost(MmonitBaseAction):
    def run(self, host_id, uptime_range=0, datefrom=0, dateto=0):
        self.login()

        if datefrom != 0 and uptime_range != 12:
            raise Exception("If datefrom is set, range should be 12")
        data = {"id": host_id, "range": uptime_range, "datefrom": datefrom, "dateto": dateto}
        req = self.session.post("{}/reports/uptime/get".format(self.url), data=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
