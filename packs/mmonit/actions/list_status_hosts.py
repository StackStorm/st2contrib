from lib.mmonit import MmonitBaseAction


class MmonitListStatusHost(MmonitBaseAction):
    def run(self, host_id=None, hostgroupid=None, status=None, platform=None, machine=None,
            led=None):
        self.login()
        data = {}

        # Way too explicit for my taste but I guess its easier to understand
        if host_id is not None:
            data['host_id'] = host_id
        if hostgroupid is not None:
            data['hostgroupid'] = hostgroupid
        if status is not None:
            data['status'] = status
        if platform is not None:
            data['platform'] = platform
        if machine is not None:
            data['machine'] = machine
        if led is not None:
            data['led'] = led

        req = self.session.get("{}/admin/hosts/update".format(self.url), params=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
