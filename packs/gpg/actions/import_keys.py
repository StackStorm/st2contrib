from lib.base import BaseGPGAction

__all__ = [
    'ImportKeysAction'
]


class ImportKeysAction(BaseGPGAction):
    def run(self, file_path):
        with open(file_path, 'r') as fp:
            key_data = fp.read()

        import_result = self._gpg.import_keys(key_data)
        # pylint: disable=no-member
        return import_result.count
