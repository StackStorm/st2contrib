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

from utils import is_ip


class OrionNode(object):
    """
    Class for holding Orion Node details.
    """
    def __init__(self):
        """
        Setup the class
        """
        self._caption = None
        self._ip_address = None
        self._npm = False
        self._ncm = False
        self._npm_id = None
        self._ncm_id = None
        self._uri = None

    def __str__(self):
        return "{} (NodeId: {}; ip: {})".format(
            self._caption,
            self._npm_id,
            self._ip_address)

    def __repr__(self):
        return self.__str__

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        if is_ip(ip_address):
            self._ip_address = ip_address
        else:
            raise ValueError("Not an IP address")

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption = caption

    @property
    def npm_id(self):
        return self._npm_id

    @npm_id.setter
    def npm_id(self, npm_id):
        """
        Set self._npm_id and update self._npm to True.
        """

        if npm_id is not None:
            self._npm_id = npm_id
            self._npm = True
        else:
            self._npm_id = None
            self._npm = False

    @property
    def ncm_id(self):
        return self._ncm_id

    @ncm_id.setter
    def ncm_id(self, ncm_id):
        """
        Set self._ncm_id and update self._ncm to True.
        """
        if ncm_id is not None:
            self._ncm_id = ncm_id
            self._ncm = True
        else:
            self._ncm_id = None
            self._ncm = False

    @property
    def npm(self):
        return self._npm

    @property
    def ncm(self):
        return self._ncm

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        self._uri = uri
