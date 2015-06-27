from lib.webpagetest import WebPageTestAction

__all__ = ['RandomTest']


class RandomTest(WebPageTestAction):
    def run(self, domain):
        return self.test_random_location(domain)
