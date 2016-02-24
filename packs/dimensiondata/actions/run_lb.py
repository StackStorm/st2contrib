from lib import actions

__all__ = [
    'LBAction',
]


class LBAction(actions.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        driver = self._get_lb_driver(region)
        return self._do_function(driver, action, **kwargs)
