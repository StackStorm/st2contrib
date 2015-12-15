from lib.actions import BaseAction


class ArticleUpdate(BaseAction):
    def run(self, slug, title, body):
        slug = self._convert_slug(slug)
        path = '/articles/%s' % slug
        payload = self._create_payload(title=title, body=body)
        response = self._api_put(path, json=payload)
        return response

    def _create_payload(self, title, body):
        payload = {
            'article': {
                'title': title,
                'body': body,
            }
        }
        return payload
