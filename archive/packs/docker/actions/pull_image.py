from lib.base import DockerBasePythonAction


__all__ = [
    'DockerPullImageAction'
]


class DockerPullImageAction(DockerBasePythonAction):
    def run(self, repo, tag=None, insecure_registry=False,
            auth_username_override=None, auth_password_override=None):
        auth_override = (auth_username_override and auth_password_override)

        if auth_override:
            auth_config = {}
            auth_config['username'] = auth_username_override
            auth_config['password'] = auth_password_override
            return self.wrapper.pull(repo=repo, tag=tag, insecure_registry=insecure_registry,
                                     auth_config=auth_config)
        else:
            return self.wrapper.pull(repo=repo, tag=tag, insecure_registry=insecure_registry)
