from lib.actions import OctopusDeployAction

__all__ = [
    'ListProjectsAction'
]


class ListProjectsAction(OctopusDeployAction):
    def run(self):
        result = self.make_get_request(action="projects/all")
        return result.get('Items', None)
