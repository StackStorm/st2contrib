from lib import action


class ListRunningJobs(action.JenkinsBaseAction):
    def run(self):
        return self.jenkins.get_jobs()
