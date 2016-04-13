from st2tests.base import BaseActionAliasTestCase


class NcmConfigDownloadActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'ncm_config_download'

    def test_ncm_config_download_alias(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]

        command = "orion ncm config-download orion router1"
        expected_parameters = {
            'platform': 'orion',
            'node': 'router1'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)

class NodeStatusActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'node_status'

    def test_node_status_alias(self):
        format_string = self.action_alias_db.formats[0]['representation'][0]
        format_strings = self.action_alias_db.formats[0]['representation']

        command = "orion node status orion router1"
        expected_parameters = {
            'platform': 'orion',
            'node': 'router1'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)

        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)

class NodeCreateActionAliasTestCase(BaseActionAliasTestCase):
    action_alias_name = 'node_create'

    def test_node_create_alias(self):
        format_strings = self.action_alias_db.formats[1]['representation']
        format_string = self.action_alias_db.formats[1]['representation'][3]

        command = "create orion node router1 at 192.168.0.1"
        expected_parameters = {
            'ip_address': "192.168.0.1",
            'node': 'router1'
        }
        self.assertExtractedParametersMatch(format_string=format_string,
                                            command=command,
                                            parameters=expected_parameters)

        self.assertCommandMatchesExactlyOneFormatString(
            format_strings=format_strings,
            command=command)
