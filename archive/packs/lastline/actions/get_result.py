from lib import actions


class GetResult(actions.BaseAction):
    def run(self, uuid, report_uuid=None, full_report_score=None,
            include_scoring_components=None, raw=False,
            requested_format='json', verify=True, report_version=None):

        response = self.client.get_result(uuid, report_uuid, full_report_score,
                                          include_scoring_components, raw,
                                          requested_format, verify,
                                          report_version)

        return response
