from lib.base import DockerBasePythonAction


__all__ = [
    'DockerPushImageAction'
]


class DockerPushImageAction(DockerBasePythonAction):
    def run(self, repo, tag=None, insecure_registry=False):
        return self.wrapper.push(repo=repo, tag=tag, insecure_registry=insecure_registry)
