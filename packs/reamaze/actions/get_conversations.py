from lib.actions import BaseAction


class GetConversations(BaseAction):
    def run(self, filter_issues='all', sort='create_at', email=None, tag=None, data=None):
        params = {
            'filter': filter_issues,
            'sort': sort,
        }
        if email:
            params['email'] = email
        if tag:
            params['tag'] = tag
        if data:
            params['data'] = data

        response = self._api_get('/conversations', params=params)
        conversations = response['conversations']

        return conversations
