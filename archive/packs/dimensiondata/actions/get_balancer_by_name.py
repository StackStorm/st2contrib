from lib import actions

__all__ = [
    'GetBalancerByNameAction',
]


class GetBalancerByNameAction(actions.BaseAction):

    def run(self, region, balancer_name):
        driver = self._get_lb_driver(region)
        balancers = driver.list_balancers()
        balancer = list(filter(lambda x: x.name == balancer_name,
                               balancers))[0]
        return self.resultsets.formatter(balancer)
