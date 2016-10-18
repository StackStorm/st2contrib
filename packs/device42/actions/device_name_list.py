from lib.base_action import BaseAction


class DeviceNameList(BaseAction):
    def run(self, type=None, service_level=None, in_service=None, customer=None, tags=None,
            blade_host_name=None, virtual_host_name=None, building_id=None, building=None,
            room_id=None, room=None, rack_id=None, rack=None, serial_no=None,
            serial_no_contains=None, asset_no=None, name=None, tags_and=None, uuid=None,
            is_it_switch=None, is_it_virtual_host=None, is_it_blade_host=None, hardware=None,
            hardware_ids=None, os=None, virtual_subtype=None, last_updated_lt=None,
            last_updated_gt=None, first_added_lt=None, first_added_gt=None,
            custom_fields_and=None, custom_fields_or=None):
        response = self.getAPI("/api/1.0/devices/", {
            "type": type,
            "service_level": service_level,
            "in_service": in_service,
            "customer": customer,
            "tags": tags,
            "blade_host_name": blade_host_name,
            "virtual_host_name": virtual_host_name,
            "building_id": building_id,
            "building": building,
            "room_id": room_id,
            "room": room,
            "rack_id": rack_id,
            "rack": rack,
            "serial_no": serial_no,
            "serial_no_contains": serial_no_contains,
            "asset_no": asset_no,
            "name": name,
            "tags_and": tags_and,
            "uuid": uuid,
            "is_it_switch": is_it_switch,
            "is_it_virtual_host": is_it_virtual_host,
            "is_it_blade_host": is_it_blade_host,
            "hardware": hardware,
            "hardware_ids": hardware_ids,
            "os": os,
            "virtual_subtype": virtual_subtype,
            "last_updated_lt": last_updated_lt,
            "last_updated_gt": last_updated_gt,
            "first_added_lt": first_added_lt,
            "first_added_gt": first_added_gt,
            "custom_fields_and": custom_fields_and,
            "custom_fields_or": custom_fields_or,
        })

        names = []
        for device in response["Devices"]:
            names.append(device["name"])

        return names
