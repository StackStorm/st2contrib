from lib.actions import OctopusDeployAction

__all__ = [
    'CreateReleaseAction'
]


class CreateReleaseAction(OctopusDeployAction):
    def run(self, project_id):
        result = self.make_post_request("releases", {"ProjectId" : project_id})
        return result
