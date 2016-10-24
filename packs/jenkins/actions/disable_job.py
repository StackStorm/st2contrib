from lib import action


class DisableProject(action.JenkinsBaseAction):
    def run(self, project):
        return self.jenkins.disable_job(project)
