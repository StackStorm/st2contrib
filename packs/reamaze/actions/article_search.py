from lib.actions import BaseAction
from dotted.utils import dot
from fuzzywuzzy import fuzz
import json


class ArticleSearch(BaseAction):
    def run(self, query, include_body=False, limit=5):
        response = self._api_get('/articles')
        articles = dot(response['articles'])

        ranks = map(self._rank_article, query, articles)
        results = sorted(ranks, key=lambda rank: rank[0], reverse=True)[:limit]
        response = map(self._extract_article_data, results,
                       include_body=include_body)

        return json.dumps(response)

    # Takes an incoming query and an article, and runs a fuzzy token
    # search to get data from an article.
    #
    # Returns a tuple of (rank, article)
    def self._rank_article(self, query, article):
        rank = fuzz.token_sort_ratio(query, article.body)
        return (rank, article)

    # Takes a tuple of (rank, article), and extracts data from the
    # object based on whether the user asks for additional body data
    # or not.
    def self._extract_article_data(self, article, include_body=False):
        article_data = (article.title, article.url)
        return article_data + article.body if include_body else article_data
