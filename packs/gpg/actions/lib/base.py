import gnupg

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseGPGAction'
]


class BaseGPGAction(Action):
    def __init__(self, config):
        super(BaseGPGAction, self).__init__(config=config)

        debug = self.config.get('debug', False)
        gpghome = self.config.get('gpghome', None)
        gpgbinary = self.config.get('gpgbinary', None)

        kwargs = {
            'verbose': debug
        }

        if gpghome:
            kwargs['gpghome'] = gpghome

        if gpgbinary:
            kwargs['gpgbinary'] = gpgbinary

        self._gpg = gnupg.GPG(**kwargs)
