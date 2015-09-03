from lib.actions import OctopusDeployAction

__all__ = [
    'CreateReleaseAction'
]


class CreateReleaseAction(OctopusDeployAction):
    def run(self, project_id, version):
        result = self.make_post_request(action="releases",
                                        payload={"ProjectId" : project_id,
                                                 "Version" : version})
        return result
