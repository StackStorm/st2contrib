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

import time

from st2actions.runners.pythonrunner import Action
from orionsdk import SwisClient


class OrionBaseAction(Action):
    def __init__(self, config):
        super(OrionBaseAction, self).__init__(config)

        self.client = None

        if "orion" not in self.config:
            raise ValueError("Orion host details not in the config.yaml")

    def connect(self, platform):
        try:
            self.client = SwisClient(self.config['orion'][platform]['host'],
                                   self.config['orion'][platform]['user'],
                                   self.config['orion'][platform]['password'])
        except KeyError:
            raise ValueError("Orion host details not in the config.yaml")

    def query(self, swql, **kargs):
        return self.client.query(swql, **kargs)

    def invoke(self, entity, verb, *args):
        return self.client.invoke(entity, verb, *args)

    def create(self, entity, **kargs):
        return self.client.create(entity, **kargs)

    def get_node_id(self, caption):
        swql = "SELECT NodeID FROM Orion.Nodes WHERE Caption=@caption"
        kargs = {'caption': caption}
        data = self.query(swql, **kargs)

        if len(data['results']) == 1:
            try:
                return data['results'][0]['NodeID']
            except IndexError:
                raise ValueError("Invalid Node")
        elif len(data['results']) >= 2:
            raise ValueError("Muliple Nodes match '{}' Caption".format(
                caption))
        elif len(data['results']) == 0:
            raise ValueError("No matching Caption for '{}'".format(
                caption))

    def get_ncm_node_id(self, caption):
        """
        Queries the Network configuration Manager nodes table on the Orion
        platform for the NodeID of a given node name (aka NodeCaption).

        Raises: IndexError on Invalid number of nodes (e.g. 0 or 2+).

        Returns: A single node id.
        """

        swql = "SELECT NodeID FROM Cirrus.Nodes WHERE NodeCaption=@node"
        kargs = {'node': caption}
        data = self.query(swql, **kargs)

        if len(data['results']) == 1:
            try:
                return data['results'][0]['NodeID']
            except IndexError:
                raise IndexError("Invalid Node")
        elif len(data['results']) >= 2:
            raise IndexError("Muliple Nodes match '{}' NodeCaption".format(
                caption))
        elif len(data['results']) == 0:
            raise IndexError("No matching NodeCaption for '{}'".format(
                caption))

    def get_ncm_transfer_results(self, transfer_id):
        ts = {}
        while True:
            swql = """SELECT TransferID, Action, Status, ErrorMessage,
            DeviceOutput FROM NCM.TransferResults
            WHERE TransferID=@transfer_id"""
            kargs = {'transfer_id': transfer_id}

            transfer_data = self.query(swql, **kargs)
            status = transfer_data['results'][0]['Status']

            if status == 1:
                time.sleep(10)
            elif status == 2:
                ts['status'] = "Complete"
                break
            elif status == 3:
                ts['status'] = "Error"
                ts['ErrorMessage'] = transfer_data['results'][0][
                    'ErrorMessage']
                break
            else:
                ts['status'] = "Unknown"
                ts['ErrorMessage'] = "Invalid stauts: {}".format(status)
                break

        return ts

    def status_code_to_text(self, status):
        """
        Takes an Solarwinds Orion status code and translates it to
        human text and also a colour that can be used in Slack.
        """

        if status == 0:
            return ("Unknown", "grey")
        elif status == 1:
            return ("Up", "good")
        elif status == 2:
            return ("Down", "danger")
        elif status == 3:
            return ("Warning", "warning")
        elif status == 14:
            return ("Critical", "danger")

    def send_user_error(self, message):
        print(message)
