from lib.actions import BaseAction
import yaml

__all__ = [
    'ConfigureAction'
]


class ConfigureAction(BaseAction):

    def run(self, api_user, api_password):
        with open('/opt/stackstorm/packs/dimensiondata/config.yaml', 'w') as outfile:
            outfile.write(yaml.safe_dump(
                {"api_user": api_user,
                 "api_password": api_password}))
