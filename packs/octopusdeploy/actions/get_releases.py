from lib.actions import OctopusDeployAction

__all__ = [
    'GetReleasesAction'
]


class GetReleasesAction(OctopusDeployAction):
    def run(self, project_id):
        result = self.make_get_request("projects/%s/releases" % project_id)
        return result['Items']
