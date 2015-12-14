from lib.actions import BaseAction


class GetConversations(BaseAction):
    CHANNEL = {
        1: 'email',
        2: 'twitter',
        3: 'facebook',
        6: 'chat',
    }

    STATUS = {
        0: 'unresolved',
        1: 'pending',
        2: 'resolved',
        3: 'spam',
        4: 'archived',
    }

    def run(self, filter_issues='open', sort='create_at', email=None, tag=None, data=None):
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

        filtered_conversations = map(self.filter_conversation, conversations)
        return filtered_conversations

    @staticmethod
    def filter_conversation(conversation):
        filtered_channel = GetConversations.CHANNEL[conversation["category"]["channel"]]
        filtered_status = GetConversations.STATUS[conversation["status"]]
        conversation["channel_name"] = filtered_channel
        conversation["status_name"] = filtered_status

        return conversation
