from lib.actions import BaseAction


class ArticleGet(BaseAction):
    def run(self, slug):
        slug = self._convert_slug(slug)
        path = '/articles/%s' % slug
        response = self._api_get(path)
        article = response['articles']

        return article
