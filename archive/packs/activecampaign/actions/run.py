import requests
import urlparse

from st2actions.runners.pythonrunner import Action


class ActiveCampaignAction(Action):

    def run(self, **kwargs):
        if kwargs['api_key'] is None:
            kwargs['api_key'] = self.config['api_key']

        return self._get_request(kwargs)

    def _get_request(self, params):
        url = urlparse.urljoin(self.config['url'], 'admin/api.php')
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        params = self._format_params(params)

        response = requests.request(
            'POST', url=url,
            headers=headers, data=params
        )

        results = response.json()
        if results['result_code'] is not 1:
            failure_reason = (
                'Failed to perform action. status code: %s; response body: %s' % (
                    response.status_code,
                    response.json
                )
            )
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return results

    def _format_params(self, params):
        output = {}
        for k, v in params.iteritems():
            if isinstance(v, dict):
                for pk, pv in v.iteritems():
                    if k == 'field':
                        param_name = "{}[%{}%,0]".format(k, pk)
                    else:
                        param_name = "%s[%s]" % (k, pk)
                    output[param_name] = pv
            else:
                if v is not None:
                    output[k] = v
        return output
