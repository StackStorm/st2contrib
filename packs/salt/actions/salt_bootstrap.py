import salt.cloud

__all__ = [
    'SaltInstaller'
]

class SaltInstaller(object):
    def run(name, provider, instance_id):
        client = salt.cloud.CloudClient('/etc/salt/cloud')
        ret = client.create(names=[name], provider=provider, instance_id=instance_id)
        return ret
