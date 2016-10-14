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

from lib.actions import OrionBaseAction
from lib.utils import send_user_error


class UpdateNodeCustomProperties(OrionBaseAction):
    def run(self, node, custom_property, value):
        """
        Update a nodes Cutom Properties.
        """
        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            msg = "Node ({}) does not exist".format(node)
            send_user_error(msg)
            raise ValueError(msg)

        current_properties = self.read(orion_node.uri + '/CustomProperties')

        if custom_property not in current_properties:
            msg = "custom property {} does not exist!".format(custom_property)
            send_user_error(msg)
            raise ValueError(msg)

        kargs = {custom_property: value}

        orion_data = self.update(orion_node.uri + '/CustomProperties', **kargs)

        # This update returns None, so check just in case.
        # This happens even if the custom_property does not exist!
        if orion_data is None:
            return True
        else:
            return orion_data
