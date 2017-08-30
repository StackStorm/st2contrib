from lib import actions


class SubmitURL(actions.BaseAction):
    def run(self, url, referer=None, full_report_score=None, bypass_cache=None,
            backend=None, analysis_timeout=None, push_to_portal_account=None,
            raw=False, verify=True, user_agent=None, report_version=None):

        response = self.client.submit_url(url, referer, full_report_score,
                                          bypass_cache, backend,
                                          analysis_timeout,
                                          push_to_portal_account, raw, verify,
                                          user_agent, report_version)

        return response
