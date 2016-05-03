# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lib.icsp import ICSPBaseActions
import eventlet


class GetJobStatus(ICSPBaseActions):
    def run(self, job_id, monitor, monitor_interval=120,
            connection_details=None):
        self.set_connection(connection_details)
        self.get_sessionid()

        output = {}
        endpoint = "/rest/os-deployment-jobs"
        if monitor and not job_id:
            raise ValueError("Unable to proceed. Monitor \
                             feature requires a single Job ID")

        if job_id:
            endpoint = endpoint + "/%s" % (job_id)

        jobs = self.icsp_get(endpoint)
        # Single Job ID doesn't have Members element
        if not job_id:
            for job in jobs['members']:
                jobid = self.extract_id(job["uri"])
                output[jobid] = job['state']
        else:
            status = jobs['state']
            if monitor:
                jobid = self.extract_id(jobs["uri"])
                while status == "STATUS_ACTIVE":
                    eventlet.sleep(monitor_interval)
                    jobs = self.icsp_get(endpoint)
                    status = jobs['state']
                if status == 'STATUS_SUCCESS':
                    output[jobid] = jobs['state']
                else:
                    raise Exception("%s: %s" % (jobid, status))
            else:
                jobid = self.extract_id(jobs["uri"])
                output[jobid] = jobs['state']

        return {"jobs": output}
