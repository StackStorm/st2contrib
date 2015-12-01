from lib.actions import BaseAction


class ArticleSearch(BaseAction):
    def run(self, query):
        params = {
            'q': query,
        }

        response = self._api_get('/articles', params=params)
        articles = response['articles']

        return articles
