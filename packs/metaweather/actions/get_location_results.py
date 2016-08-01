import requests
from st2actions.runners.pythonrunner import Action


__all__ = [
    'GetLocationResultsAction'
]


class GetLocationResultsAction(Action):
    def run(self, query):
        results = requests.get('https://www.metaweather.com/api/location/search/?query=%s' % (query))

        if results.status_code != 200:
            raise Exception("Call to MetaWeather failed.")

        result = results.json()
        return result
