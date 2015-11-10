import urllib

import requests

from st2actions.runners.pythonrunner import Action

__all__ = [
    'SendInviteAction'
]


class SendInviteAction(Action):
    def run(self, email, channels, first_name, token, set_active, attempts):
        token = token if token else self.config['admin']['admin_token']
        set_active = set_active if set_active else self.config['admin']['set_active']
        attempts = attempts if attempts else self.config['admin']['attempts']
        auto_join_channels = self.config['admin']['auto_join_channels']
        url = "https://%s.slack.com/api/users.admin.invite" % \
            self.config['admin']['organization']

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = {
            'email': email.encode('utf-8'),
            'channels': " ".join(auto_join_channels),
            'first_name': first_name.encode('utf-8'),
            'token': token,
            'set_active': set_active,
            '_attempts': attempts
        }

        data = urllib.urlencode(body)
        response = requests.get(url=url,
                                headers=headers, params=data)
        results = response.json()

        if results['ok'] is True:
            return 'Invite successfully sent to %s. RESPONSE: %s' % \
                (email, results)
        else:
            failure_reason = ('Failed to send invite to %s: %s \
                              (status code: %s)' % (email, response.text,
                              response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return True
