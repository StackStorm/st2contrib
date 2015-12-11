import json

from lib.actions import BaseAction


class ArticleGet(BaseAction):
    def run(self, title, body, topic=None, status=0):
        if topic:
            topic = self._convert_slug(topic)
            path = '/topics/%s/articles' % topic
        else:
            path = '/articles'
        payload = self._create_payload(title=title, body=body, status=status)
        response = self._api_post(path, data=payload)
        article = response['articles']

        return article

    def _validate_article(self, title, body, status=0):
        payload = {
            'article': {
                'title': title,
                'body': body,
                'status': status
            }
        }
        return json.dumps(payload)
