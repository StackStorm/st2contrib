from lib.webpagetest import WebPageTestAction

__all__ = ['ListLocations']


class ListLocations(WebPageTestAction):
    def run(self):
        return self.list_locations()
