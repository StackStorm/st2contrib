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

import atexit
import eventlet

from pyVim import connect
from pyVmomi import vim
from st2actions.runners.pythonrunner import Action

CONNECTION_ITEMS = ['host', 'port', 'user', 'passwd']


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config is None:
            raise ValueError("No connection configuration details found")
        if "vsphere" in config:
            if config['vsphere'] is None:
                raise ValueError("'vsphere' config defined but empty.")
            else:
                pass
        else:
            for item in CONNECTION_ITEMS:
                if item in config:
                    pass
                else:
                    raise KeyError("Config.yaml Mising: %s" % (item))

    def establish_connection(self, vsphere):
        self.si = self._connect(vsphere)
        self.si_content = self.si.RetrieveContent()

    def _connect(self, vsphere):
        if vsphere:
            connection = self.config['vsphere'].get(vsphere)
            for item in CONNECTION_ITEMS:
                if item in connection:
                    pass
                else:
                    raise KeyError("Config.yaml Mising: vsphere:%s:%s"
                                   % (vsphere, item))
        else:
            connection = self.config

        try:
            si = connect.SmartConnect(host=connection['host'],
                                      port=connection['port'],
                                      user=connection['user'],
                                      pwd=connection['passwd'])
        except Exception as e:
            raise Exception(e)

        atexit.register(connect.Disconnect, si)
        return si

    def _wait_for_task(self, task):
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        return task.info.state == vim.TaskInfo.State.success
