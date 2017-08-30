from libcloud.compute.base import NodeAuthPassword
from libcloud.common.dimensiondata import DimensionDataServerCpuSpecification
from lib import actions

__all__ = [
    'CreateVMMcp1Action',
]


class CreateVMMcp1Action(actions.BaseAction):

    def run(self, region, location, network_id, image_name,
            name,
            description, is_started, password,
            memory_gb, cpu_count, cpu_speed, cores_per_socket):
        driver = self._get_compute_driver(region)
        root_pw = NodeAuthPassword(password)
        location = driver.ex_get_location_by_id(location)

        images = driver.list_images(location=location)

        image = list(filter(lambda x: x.name == image_name,
                            images))[0]
        networks = driver.list_networks(location)
        network = list(filter(lambda x: x.id == network_id,
                              networks))[0]
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
                                  ex_network=network,
                                  ex_cpu_specification=cpu,
                                  ex_memory_gb=memory_gb,
                                  ex_is_started=is_started)
        return self.resultsets.formatter(node)
