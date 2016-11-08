from lib import action


class EnableProject(action.JenkinsBaseAction):
    def run(self, name):
        return self.jenkins.enable_job(name)
