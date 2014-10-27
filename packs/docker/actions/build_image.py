import os

from lib.base import DockerBasePythonAction


__all__ = [
    'DockerBuildImageAction'
]


class DockerBuildImageAction(DockerBasePythonAction):
    def run(self, dockerfile_path, tag):
        if os.path.isdir(dockerfile_path):
            return self.wrapper.build(path=dockerfile_path, tag=tag)
        else:
            return self.wrapper.build(fileobj=dockerfile_path, tag=tag)
