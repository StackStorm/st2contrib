#!/usr/bin/env python

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
import duo_client


class Check(Action):
    def run(self):
        """
        Ping the Duo Platorm.

        Returns: An dict with info returned by Duo.

        Raises:
          ValueError: On Auth Failure.
        """

        try:
            ikey = self.config['ikey']
            skey = self.config['skey']
            host = self.config['host']
        except KeyError:
            raise ValueError("Duo config not found in config.")

        auth = duo_client.Auth(ikey=ikey,
                               skey=skey,
                               host=host)

        try:
            data = auth.check()
        except:
            raise ValueError("Ping failed!")
        else:
            return data
