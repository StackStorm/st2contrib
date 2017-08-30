from lib.mmonit import MmonitBaseAction


class MmonitUpdateHost(MmonitBaseAction):
    def run(self, host_id, hostname, keepname=None, description=None, status=None, ipaddrout=None,
            portout=None, sslout=None, monituser=None, monitpassword=None, skew=None):
        self.login()
        data = {"id": host_id, "hostname": hostname}

        # Way too explicit for my taste but I guess its easier to understand
        if keepname is not None:
            data['keepname'] = keepname
        if description is not None:
            data['description'] = description
        if status is not None:
            data['status'] = status
        if ipaddrout is not None:
            data['ipaddrout'] = ipaddrout
        if portout is not None:
            data['portout'] = portout
        if sslout is not None:
            data['sslout'] = sslout
        if monituser is not None:
            data['monituser'] = monituser
        if monitpassword is not None:
            data['monitpassword'] = monitpassword
        if skew is not None:
            data['skew'] = skew

        req = self.session.post("{}/admin/hosts/update".format(self.url), data=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
