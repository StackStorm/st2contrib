from lib.actions import OctopusDeployAction

__all__ = [
    'ListReleasesAction'
]


class ListReleasesAction(OctopusDeployAction):
    def run(self, project_id):
        result = self.make_get_request(action="projects/%s/releases"
                                       % project_id)
        return result.get('Items', [])
