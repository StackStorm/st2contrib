from lib.icsp import ICSPBaseActions
import eventlet
import json


class GetJobStatus(ICSPBaseActions):
    def run(self, job_id, monitor, connection_details):
        if connection_details:
            self.setConnection(connection_details)
        self.getSessionID()

        output = {}
	endpoint = "/rest/os-deployment-jobs"
        if monitor and not job_id:
            raise ValueError("Unable to proceed. Monitor feature requires a single Job ID")

        if job_id:
            endpoint = endpoint + "/%s" % job_id

        jobs = self.icspGET(endpoint)
        # Single Job ID doesn't have Members element
        if not job_id:
            for job in jobs['members']:
                jobid = job["uri"].split("/")[-1]
                output[jobid] = job['state']
        else:
            status = jobs['state']
            if monitor:
                jobid = jobs["uri"].split("/")[-1]
                while status == "STATUS_ACTIVE":
                    eventlet.sleep(120)
                    jobs = self.icspGET(endpoint)
                    status = jobs['state']
                output[jobid] = jobs['state']
            else:
                jobid = jobs["uri"].split("/")[-1]
                output[jobid] = jobs['state']

        return {"jobids": output}
