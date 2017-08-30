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

from st2actions.runners.pythonrunner import Action


class IsValidIpPortAction(Action):
    def run(self, port):
        """
        args:
        - port (int): a IP port number to check if valid.

        raises:
        - ValueError: For invalid ports.

        returns:
        - True: If a valid port.
        """

        if port < 0:
            raise ValueError("Invalid port: {} is less than 0.".format(port))
        elif port > 65535:
            raise ValueError("Invalid port: {} is greater than 65535.".format(port))
        else:
            return True
