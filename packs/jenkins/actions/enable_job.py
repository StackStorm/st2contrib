from lib import action


class EnableProject(action.JenkinsBaseAction):
    def run(self, project):
        return self.jenkins.enable_job(project)
