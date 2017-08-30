from subprocess import Popen, PIPE
import platform
import os


class LocateBinary(object):
    """Class implements lookup for chef binaries.
    """

    def locate_binary(self, binary):
        """Locate full path of a chef binary
        """
        # Try sane paths
        for base_path in self._sane_paths():
            path = os.path.join(base_path, binary)
            if platform.system() == 'Windows' and os.path.isfile(path):
                return path
            elif os.path.isfile(path):
                # On *nix file must be executable
                if not os.access(path, os.X_OK):
                    raise RuntimeError('File %s must have premission to be executed', path)
                return path

        # Do which for the last resort
        if platform.system() == 'Windows':
            # Ignore scripts and etc, binary must be an executable file
            env, which = ({'PATHEXT': '.exe'}, 'where')
        else:
            env, which = (None, 'which')

        proc = Popen([which, binary], stdout=PIPE, env=env, shell=False)
        stdout, _ = proc.communicate()
        if proc.returncode > 0:
            raise RuntimeError("File `{}' not found".format(binary))

        return stdout.rstrip()

    @staticmethod
    def _sane_paths():
        if platform.system() == 'Windows':
            return ()
        else:
            return ('/usr/local/sbin', '/usr/local/bin', '/usr/sbin', '/usr/bin', '/sbin', '/bin')
