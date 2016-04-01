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

import eventlet

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class WaitTask(BaseAction):

    def run(self, task_id):
        # convert ids to stubs
        task = inventory.get_task(self.si_content, moid=task_id)
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        result, error = None, None
        if task.info.state == vim.TaskInfo.State.success:
            result = task.info.result
        else:
            error = task.info.error
        return {'result': result, 'error': error}
