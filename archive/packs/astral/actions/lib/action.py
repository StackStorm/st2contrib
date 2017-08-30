"""
Copyright 2016 Brocade Communications Systems, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from st2actions.runners.pythonrunner import Action
from astral import Location


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._latitude = self.config['latitude']
        self._longitude = self.config['longitude']
        self._timezone = self.config['timezone']

        location = Location(('name', 'region', float(self._latitude),
                            float(self._longitude), self._timezone, 0))

        self.sun = location.sun()
