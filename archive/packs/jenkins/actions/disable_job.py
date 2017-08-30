from lib import action


class DisableProject(action.JenkinsBaseAction):
    def run(self, name):
        return self.jenkins.disable_job(name)
