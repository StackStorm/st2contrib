from lib.actions import OctopusDeployAction

__all__ = [
    'GetDeploymentsAction'
]


class GetDeploymentsAction(OctopusDeployAction):
    def run(self, project_id):
        result = self.make_get_request(action="deployments?projects="
                                       % project_id)
        return result['Items']
