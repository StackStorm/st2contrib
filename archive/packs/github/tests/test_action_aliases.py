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

from st2tests.base import BaseActionAliasTestCase


class CreateDeployment(BaseActionAliasTestCase):
    action_alias_name = "create_deployment"

    def test_alias_create_deployment_simple(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github deployment create st2contrib description A description"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': None,
            'ref': "master",
            'environment': "production",
            'description': "A description"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_create_deployment_full(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github deployment create st2contrib type online ref v1.0.0 environment staging description Another description"  # NOQA
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': "online",
            'ref': "v1.0.0",
            'environment': "staging",
            'description': "Another description"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class CreateRelease(BaseActionAliasTestCase):
    action_alias_name = "create_release"

    def test_alias_create_release_simple(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github release create st2contrib name v1.0.0 body It's a release Jim, but not as we know it!"  # NOQA
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': None,
            'name': "v1.0.0",
            'version_increase': None,
            'target_commitish': None,
            'body': "It's a release Jim, but not as we know it!"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_create_release_full(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github release create st2contrib type online version patch commit master name v1.0.0 body It's a release Jim, but not as we know it!"  # NOQA
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': "online",
            'version_increase': "patch",
            'target_commitish': "master",
            'name': "v1.0.0",
            'body': "It's a release Jim, but not as we know it!"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class DeploymentStatuses(BaseActionAliasTestCase):
    action_alias_name = "deployment_statuses"

    def test_alias_deployment_statuses_simple(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github deployment statuses st2contrib id 1"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': None,
            'deployment_id': "1",
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_deployment_statuses_full(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github deployment statuses type online st2contrib id 1"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': "online",
            'deployment_id': "1",
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class GetUser(BaseActionAliasTestCase):
    action_alias_name = "get_user"

    def test_alias_get_user_simple(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github get user stanley"
        expected_parameters = {
            'user': "stanley",
            'github_type': None
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_get_user_full(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github get user type online stanley"
        expected_parameters = {
            'user': "stanley",
            'github_type': "online"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class LatestRelease(BaseActionAliasTestCase):
    action_alias_name = "latest_release"

    def test_alias_latest_release_simple(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github release latest st2contrib"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': None
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_latest_release_full(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github release latest type online st2contrib"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': "online"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class ListRelease(BaseActionAliasTestCase):
    action_alias_name = "list_releases"

    def test_alias_list_release_simple(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github releases list st2contrib"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': None
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_list_release_full(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github releases list type online st2contrib"
        expected_parameters = {
            'repository': "st2contrib",
            'github_type': "online"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)


class StoreOauthToken(BaseActionAliasTestCase):
    action_alias_name = "store_oauth_token"

    def test_alias_store_oauth_token_default(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github store token foobar"
        expected_parameters = {
            'token': "foobar",
            'github_type': None
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_store_oauth_token_online(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github store type online token foobar"
        expected_parameters = {
            'token': "foobar",
            'github_type': "online"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

    def test_alias_store_oauth_token_enterprise(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.get_format_strings()

        command = "github store type enterprise token foobar"
        expected_parameters = {
            'token': "foobar",
            'github_type': "enterprise"
        }

        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)
        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)
