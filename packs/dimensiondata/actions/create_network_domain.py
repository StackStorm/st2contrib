from lib import actions

__all__ = [
    'CreateNetworkDomainAction',
]


class CreateNetworkDomainAction(actions.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        location_id = kwargs['location']
        del kwargs['location']
        driver = self._get_compute_driver(region)
        location = driver.ex_get_location_by_id(str(location_id))
        kwargs['location'] = location
        return self._do_function(driver, action, **kwargs)
