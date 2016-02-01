from lib.actions import BaseAction


class ArticleCreate(BaseAction):
    def run(self, title, body, topic=None, status=0):
        if topic:
            topic = self._convert_slug(topic)
            path = '/topics/%s/articles' % topic
        else:
            path = '/articles'
        payload = self._create_article(title=title, body=body, status=status)
        response = self._api_post(path, json=payload)
        return response

    def _create_article(self, title, body, status=0):
        payload = {
            'article': {
                'title': title,
                'body': body,
                'status': int(status)
            }
        }
        return payload
