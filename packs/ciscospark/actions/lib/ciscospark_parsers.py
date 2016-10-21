__all__ = [
    'CiscoSparkResultSets'
]


FIELD_LIST_MAP = {
    'Room': ['id', 'title', 'type', 'isLocked',
             'lastActivity', 'created', 'creatorId',
             'teamId'],
    'Team': ['id', 'name', 'created'],
    'Webhook': ['id', 'name', 'targetUrl', 'resource',
                'event', 'filter', 'secret', 'created',
                'data'],
    'Message': ['id', 'roomId', 'roomType', 'toPersonId', 'toPersonEmail',
                'text', 'markdown', 'files', 'personId', 'personEmail',
                'created', 'mentionedPeople']
}


class CiscoSparkResultSets(object):

    def selector(self, output):
        try:
            field_list = FIELD_LIST_MAP.get(output.__name__)
            return self.parse(output, field_list)
        except KeyError:
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
