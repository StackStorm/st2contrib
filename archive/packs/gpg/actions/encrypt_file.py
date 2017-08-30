from lib.base import BaseGPGAction

__all__ = [
    'EncryptFileAction'
]


class EncryptFileAction(BaseGPGAction):
    def run(self, file_path, recipients, output_path):
        with open(file_path, 'rb') as stream:
            self._gpg.encrypt_file(stream, recipients=recipients,
                                   output=output_path,
                                   always_trust=True)
