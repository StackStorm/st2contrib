from lib import action


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, branch="master"):
        return self.jenkins.build_job(project, {'branch': branch})
