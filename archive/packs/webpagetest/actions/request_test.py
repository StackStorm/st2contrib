from lib.webpagetest import WebPageTestAction

__all__ = ['RequestTest']


class RequestTest(WebPageTestAction):
    def run(self, domain, location):
        return self.request_test(domain, location)
