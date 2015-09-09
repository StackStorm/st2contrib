from lib.mmonit import MmonitBaseAction


class MmonitListEvents(MmonitBaseAction):
    def run(self, active=None, hostid=None, hostgroupid=None, servicenameid=None,
            servicegroupid=None, servicetype=None, eventtype=None, state=None, datefrom=None,
            results=None, startindex=None, sort_key=None, sort_dir=None, dateto=None):
        self.login()
        data = {}

        if active is not None:
            data['active'] = active
        if hostid is not None:
            data['description'] = hostid
        if hostgroupid is not None:
            data['hostgroupid'] = hostgroupid
        if servicenameid is not None:
            data['servicenameid'] = servicenameid
        if servicegroupid is not None:
            data['servicegroupid'] = servicegroupid
        if servicetype is not None:
            data['servicetype'] = servicetype
        if eventtype is not None:
            data['eventtype'] = eventtype
        if state is not None:
            data['state'] = state
        if datefrom is not None:
            data['datefrom'] = datefrom
        if results is not None:
            data['results'] = results
        if startindex is not None:
            data['startindex'] = startindex
        if sort_key is not None:
            data['sort'] = sort_key
        if sort_dir is not None:
            data['dir'] = sort_dir
        if dateto is not None:
            data['dateto'] = dateto

        req = self.session.post("{}/reports/events/list".format(self.url), data=data)

        try:
            return req.json()
        except Exception:
            raise
        finally:
            self.logout()
