import gnupg

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseGPGAction'
]


class BaseGPGAction(Action):
    def __init__(self, config):
        super(BaseGPGAction, self).__init__(config=config)

        debug = self._config.get('debug', False)
        gpghome = self._config.get('gpghome', None)
        gpgbinary = self._config.get('gpgbinary', None)

        kwargs = {
            'verbose': debug
        }

        if gpghome:
            kwargs['gpghome'] = gpghome

        if gpgbinary:
            kwargs['gpgbinary'] = gpgbinary

        self._gpg = gnupg.GPG(**kwargs)
