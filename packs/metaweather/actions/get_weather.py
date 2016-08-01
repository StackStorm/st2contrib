import requests
from st2actions.runners.pythonrunner import Action


__all__ = [
    'GetWeatherAction'
]


class GetWeatherAction(Action):
    def run(self, woeid):
        results = requests.get('https://www.metaweather.com/api/location/%s/' % (woeid))

        if results.status_code != 200:
            raise Exception("Call to MetaWeather failed.")

        result = results.json()
        return result
