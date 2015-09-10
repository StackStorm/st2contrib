from lib.actions import OctopusDeployAction

__all__ = [
    'DeployReleaseAction'
]


class DeployReleaseAction(OctopusDeployAction):
    def run(self, release_id, environment_id):
        result = self.make_post_request(action="deployments",
                                        payload={"ReleaseId": release_id,
                                                 "EnvironmentId": environment_id})
        return result
