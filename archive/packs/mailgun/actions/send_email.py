import httplib

import requests

from st2actions.runners.pythonrunner import Action

__all__ = [
    'SendEmailAction'
]

SEND_EMAIL_API_URL = 'https://api.mailgun.net/v2/%(domain)s/messages'


class SendEmailAction(Action):
    def run(self, sender, recipient, subject, text=None, html=None):
        if not text and not html:
            raise ValueError('Either "text" or "html" or both arguments need to be provided')

        domain = self.config['domain']
        api_key = self.config['api_key']

        data = {
            'from': sender,
            'to': recipient,
            'subject': subject
        }

        if text:
            data['text'] = text

        if html:
            data['html'] = html

        api_url = SEND_EMAIL_API_URL % {'domain': domain}
        response = requests.post(api_url, auth=('api', api_key), data=data)

        if response.status_code != httplib.OK:
            msg = ('Failed to send message (status_code=%s): %s' %
                   (response.status_code, response.text))
            raise Exception(msg)

        return True
