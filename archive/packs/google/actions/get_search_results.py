import json

from google import google

from st2actions.runners.pythonrunner import Action

from lib.formatters import google_result_to_dict

__all__ = [
    'GetSearchResultsAction'
]


class GetSearchResultsAction(Action):
    def run(self, query, count=10):
        num_page = 1

        results = google.search(query, num_page)[:count]
        result = [google_result_to_dict(obj=obj) for obj in results]
        result = json.dumps(result)
        return result
