# From https://www.reamaze.com/api/post_messages

from lib.actions import BaseAction


class CreateMessage(BaseAction):
    VISIBILITY = {
        'internal': 1,
        'regular': 0,
    }

    def run(self, slug, message, visibility='internal',
            suppress_notification=False):

        payload = {
            'message': {
                'body': message,
                'visibility': CreateMessage.VISIBILITY[visibility]
            }
        }

        if suppress_notification:
            payload['suppress_notificiaton'] = True

        endpoint = '/conversations/{}/messages'.format(slug)
        response = self._api_post(endpoint, json=payload)

        return response
