from st2actions.runners.pythonrunner import Action

from lib.docker_wrapper import DockerWrapper

__all__ = [
    'DockerBasePythonAction'
]


class DockerBasePythonAction(Action):
    def __init__(self, config):
        super(DockerBasePythonAction, self).__init__(config=config)
        self.wrapper = DockerWrapper(docker_opts=self.config)
