from lib.actions import BaseAction
from dotted.utils import dot
from fuzzywuzzy import fuzz
from functools import partial
import json
import pprint


class ArticleSearch(BaseAction):
    def run(self, query, include_body=False, limit=5):
        response = self._api_get('/articles')
        articles = response['articles']

        ranks_fun = partial(self._rank_article, query=query)
        ranks = map(ranks_fun, articles)

        results = sorted(ranks, key=lambda rank: rank[0], reverse=True)[:limit]
        response_fun = partial(self._extract_article_data,
                               include_body=include_body)
        response = map(response_fun, results)
        return json.dumps(response)

    # Takes an incoming query and an article, and runs a fuzzy token
    # search to get data from an article.
    #
    # Returns a tuple of (rank, article)
    def _rank_article(self, article, query):
        rank = fuzz.token_set_ratio(query, article['body'].encode('utf-8'))
        return (rank, article)

    # Takes a tuple of (rank, article), and extracts data from the
    # object based on whether the user asks for additional body data
    # or not.
    def _extract_article_data(self, result, include_body=False):
        article = result[1]

        article_data = {
            'title': article['title'],
            'url': article['url'],
        }
        if include_body:
            article_data['body'] = article['body']

        return article_data

