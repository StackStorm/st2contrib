from lib.base import BaseGPGAction

__all__ = [
    'DecryptFileAction'
]


class DecryptFileAction(BaseGPGAction):
    def run(self, file_path, output_path, passphrase=None):
        with open(file_path, 'rb') as stream:
            self._gpg.decrypt_file(stream, output=output_path,
                                   passphrase=passphrase)

        return True
