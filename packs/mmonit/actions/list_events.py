from lib.mmonit import MmonitBaseAction


class MmonitListEvents(MmonitBaseAction):
    def run(self, **kwargs):
        self.login()
        data = {}
        # Way too explicit for my taste but I guess its easier to understand
        if 'active' in kwargs:
            data['active'] = kwargs['active']
        if 'hostid' in kwargs:
            data['description'] = kwargs['hostid']
        if 'hostgroupid' in kwargs:
            data['hostgroupid'] = kwargs['hostgroupid']
        if 'servicenameid' in kwargs:
            data['servicenameid'] = kwargs['servicenameid']
        if 'servicegroupid' in kwargs:
            data['servicegroupid'] = kwargs['servicegroupid']
        if 'servicetype' in kwargs:
            data['servicetype'] = kwargs['servicetype']
        if 'eventtype' in kwargs:
            data['eventtype'] = kwargs['eventtype']
        if 'state' in kwargs:
            data['state'] = kwargs['state']
        if 'datefrom' in kwargs:
            data['datefrom'] = kwargs['datefrom']
        if 'results' in kwargs:
            data['results'] = kwargs['results']
        if 'startindex' in kwargs:
            data['startindex'] = kwargs['startindex']
        if 'sort_key' in kwargs:
            data['sort'] = kwargs['sort_key']
        if 'sort_dir' in kwargs:
            data['dir'] = kwargs['sort_dir']

        req = self.session.post("{}/reports/events/list".format(self.url), data=data)

        try:
            return req.json()
        except Exception as error:
            return error.message
        finally:
            self.logout()