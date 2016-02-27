from qualysapi.api_objects import *


class FieldLists():
    HOST = ['dns', 'id', 'ip', 'last_scan', 'netbios', 'os', 'tracking_method']
    SCAN = ['assetgroups', 'duration', 'launch_datetime', 'option_profile',
            'processed', 'ref', 'status', 'target',
            'title', 'type', 'user_login']
    REPORT = ['expiration_datetime', 'id', 'launch_datetime', 'output_format',
              'size', 'status', 'type', 'user_login']


class ResultSets(object):

    def selector(self, output):
        if isinstance(output, Host):
            return self.parse(output, FieldLists.HOST)
        elif isinstance(output, Scan):
            return self.parse(output, FieldLists.SCAN)
        elif isinstance(output, Report):
            return self.parse(output, FieldLists.REPORT)
        else:
            return output

    def formatter(self, output):
        formatted = []
        if isinstance(output, list):
            for o in output:
                formatted.append(self.selector(o))
        else:
            formatted = self.selector(output)
        return formatted

    def _getval(self, obj, field):
        return self.selector(getattr(obj, field))

    def parse(self, output, field_list):
        instance_data = {field: self._getval(output, field) for field in field_list}
        return instance_data
