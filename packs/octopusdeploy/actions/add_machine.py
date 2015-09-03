from lib.actions import OctopusDeployAction

__all__ = [
    'AddMachineAction'
]


class AddMachineAction(OctopusDeployAction):
    def run(self, environment_id, name, uri, thumbprint, roles):
        role_list = roles.replace(' ', '').split(',')
        payload = {
            'Name': name,
            'Thumbprint': thumbprint,
            'Uri': uri,
            'Roles': role_list,
            'IsDisabled': False,
            'EnvironmentIds': {environment_id}
        }

        result = self.make_post_request(action="machines",
                                        payload=payload)
        return result
