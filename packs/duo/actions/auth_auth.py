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

import urllib

from lib.actions import AuthAction


class Auth(AuthAction):
    def run(self, username, factor,
            ipaddr, device, push_type, passcode, pushinfo):
        """
        Auth against the Duo Platorm.

        Returns: An dict with info returned by Duo.

        Raises:
          ValueError: 'Duo config not found in config' or 'Invalid factor'
          RuntimeError: 'Failed auth.'
        """

        auth_kargs = {}

        if factor == "auto" or factor == "push":
            auth_kargs['type'] = push_type
            auth_kargs['device'] = device

            if ipaddr is not None:
                auth_kargs['ipaddr'] = ipaddr

            if pushinfo is not None:
                encoded = urllib.urlencode(pushinfo)
                auth_kargs['pushinfo'] = encoded
        elif factor == "passcode":
            auth_kargs['passcode'] = passcode
        elif factor == "phone":
            auth_kargs['device'] = device
        elif factor == "sms":
            # As 'sms' just denies and then we do not support it
            # requires re-authentication.

            raise ValueError("Denied, we do not support SMS!")
        else:
            raise ValueError("Invalid factor!")

        try:
            data = self.duo_auth.auth(factor=factor,
                                      username=username,
                                      **auth_kargs)
        except RuntimeError, e:
            raise RuntimeError("Error: %s" % e)
        else:
            if data['result'] == "allow":
                return data
            elif data['result'] == "deny":
                self.send_user_error(data['status_msg'])
                raise RuntimeError("{}".format(
                    data['status_msg']))
            else:
                raise RuntimeError("Invalid status")
