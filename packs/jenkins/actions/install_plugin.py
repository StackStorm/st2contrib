from lib import action


class InstallPlugin(action.JenkinsBaseAction):
    def run(self, plugin):
        return self.jenkins.install_plugin(plugin, include_dependencies='True')
