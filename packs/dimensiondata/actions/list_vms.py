from lib import actions

__all__ = [
    'ListVMsAction',
]


class ListVMsAction(actions.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        driver = self._get_compute_driver(region)
        kwargs['ex_location'] = str(kwargs['ex_location'])
        return self._do_function(driver, action, **kwargs)
