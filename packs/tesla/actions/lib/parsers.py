from pytesla import Vehicle

__all__ = [
    'FieldLists',
    'ResultSets'
]


class FieldLists(object):
    """
    The lists of fields we want to return for each class
    """
    VEHICLE = ['id', 'vin', 'mobile_enabled',
               'charge_state', 'climate_state',
               'drive_state', 'vehicle_state']


class ResultSets(object):

    def selector(self, output):
        if isinstance(output, Vehicle):
            return self.parse(output, FieldLists.VEHICLE)
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
        instance_data = {field: self._getval(output, field)
                         for field in field_list}
        return instance_data
