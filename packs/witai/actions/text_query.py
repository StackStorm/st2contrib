from st2actions.runners.pythonrunner import Action
import wit
import json


class TextQueryAction(Action):
    def __init__(self, config):
        super(TextQueryAction, self).__init__(config)
        self._applications = self.config.get('applications', {})
        self._default_application = self.config.get('default_application',
                                                    None)

    def run(self, text, application=None):
        if not application and self._default_application:
            app = self._default_application
        elif application:
            app = application
        else:
            raise Exception('Unknown application: %s' % application)

        access_token = self._applications.get(app, None)
        if not access_token:
            raise Exception('Missing API key for application %s' % application)

        wit.init()
        response = wit.text_query(text, access_token)
        wit.close()

        return json.loads(response)
