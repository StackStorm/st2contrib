from lib import action


class GetJobInfo(action.JenkinsBaseAction):
    def run(self, project):
        return self.jenkins.get_job_info(project, depth=0, fetch_all_builds='False')
