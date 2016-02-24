from lib import actions
from libcloud.compute.drivers.dimensiondata import (
    DimensionDataFirewallRule,
    DimensionDataFirewallAddress)

__all__ = [
    'CreateFirewallRuleAction',
]


class CreateFirewallRuleAction(actions.BaseAction):

    def run(self, **kwargs):
        network_domain_id = kwargs['network_domain_id']
        del kwargs['network_domain_id']
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        driver = self._get_compute_driver(region)
        network_domain = driver.ex_get_network_domain(network_domain_id)
        kwargs['network_domain'] = network_domain
        any_source = kwargs['any_source']
        del kwargs['any_source']
        any_destination = kwargs['any_destination']
        del kwargs['any_destination']
        if any_source:
            source = DimensionDataFirewallAddress(
                any_ip=True,
                ip_address=None,
                port_begin=None,
                port_end=None,
                ip_prefix_size=None
            )
        else:
            source = DimensionDataFirewallAddress(
                any_ip=True,
                ip_address=kwargs['source_ip'],
                port_begin=kwargs['source_port_begin'],
                port_end=['source_port_end'],
                ip_prefix_size=['source_ip_prefix_size']
            )
        if any_destination:
            destination = DimensionDataFirewallAddress(
                any_ip=True,
                ip_address=None,
                port_begin=None,
                port_end=None,
                ip_prefix_size=None
            )
        else:
            destination = DimensionDataFirewallAddress(
                any_ip=True,
                ip_address=kwargs['destination_ip'],
                port_begin=kwargs['destination_port_begin'],
                port_end=['destination_port_end'],
                ip_prefix_size=['destination_ip_prefix_size']
            )
        # setup the rule
        rule = DimensionDataFirewallRule(
            id=None,
            location=network_domain.location,
            status=None,
            network_domain=network_domain,
            enabled=True,
            source=source,
            destination=destination,
            protocol=kwargs['protocol'],
            name=kwargs['name'],
            action=kwargs['fw_action'],
            ip_version=kwargs['ip_version']
        )
        kwargs['rule'] = rule
        del kwargs['name']
        del kwargs['fw_action']
        del kwargs['ip_version']
        del kwargs['protocol']
        del kwargs['source_ip']
        del kwargs['source_port_begin']
        del kwargs['source_port_end']
        del kwargs['source_ip_prefix_size']
        del kwargs['destination_ip']
        del kwargs['destination_port_begin']
        del kwargs['destination_port_end']
        del kwargs['destination_ip_prefix_size']
        return self._do_function(driver, action, **kwargs)
