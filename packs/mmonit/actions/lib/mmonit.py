from libcloud.compute.providers import Provider
from libcloud.compute.providers import get_driver
from st2actions.runners.pythonrunner import Action
import requests


class MmonitBaseAction(Action):
    def __init__(self, config):
        super(MmonitBaseAction, self).__init__(config=config)
        self.user = config['username']
        self.password = config['password']
        self.url = config['host']
        self.session = requests.session()

    def login(self):
        self.session.get(self.url)
        login = self.session.get("{}/z_security_check".format(self.url), data={"z_csrf_protection": "off",
                                                                               "z_username": self.user,
                                                                               "z_password": self.password})
        if login.status_code != 200:
            raise Exception("Could not login to mmonit {}.".format(login.reason))

    def logout(self):
        self.session.get("{}/login/logout.csp".format(self.url))
        self.session.close()

    def run(self, **kwargs):
        raise NotImplemented("You need to override this in your class.")