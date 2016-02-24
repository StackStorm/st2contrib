from libcloud.compute.base import NodeAuthPassword, NodeState
from libcloud.common.dimensiondata import DimensionDataServerCpuSpecification
from lib import actions
from time import sleep

__all__ = [
    'CreateVMMcp2Action',
]


class CreateVMMcp2Action(actions.BaseAction):

    def run(self, region, location, network_domain_id,
            name,
            vlan_id, image_name,
            description, is_started, password,
            memory_gb, cpu_count, cpu_speed, cores_per_socket):
        driver = self._get_compute_driver(region)
        root_pw = NodeAuthPassword(password)
        location = driver.ex_get_location_by_id(location)

        images = driver.list_images(location=location)

        image = list(filter(lambda x: x.name == image_name,
                            images))[0]
        network_domain = driver.ex_get_network_domain(network_domain_id)
        vlan = driver.ex_get_vlan(vlan_id)
        cpu = None
        if cpu_count is not None:
            cpu = DimensionDataServerCpuSpecification(
                cpu_count=cpu_count,
                cores_per_socket=cores_per_socket,
                performance=cpu_speed
            )

        node = driver.create_node(name=name, image=image,
                                  auth=root_pw,
                                  ex_description=description,
                                  ex_network_domain=network_domain,
                                  ex_vlan=vlan,
                                  ex_cpu_specification=cpu,
                                  ex_memory_gb=memory_gb,
                                  ex_is_started=is_started)
        timeout = 1200  # 20 minutes
        poll_interval = 5
        cnt = 0
        while cnt < timeout / poll_interval:
            result = driver.ex_get_node_by_id(node.id)
            if result.state is NodeState.RUNNING:
                return self.resultsets.formatter(result)
            sleep(poll_interval)
            cnt += 1
        raise Exception("Timed out creating server")
