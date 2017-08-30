import pipes
import shellhelpers as shell


class Omnibus(object):
    OMNITRUCK = 'https://www.chef.io/chef/install.sh'

    def __init__(self, options):
        supports = ('pre_release', 'version', 'download_path')
        self.options = {k: options[k] for k in supports}

    def build_command(self, version=None, pre_release=False,
                      download_path=None):
        command = "curl -sL %s | sudo bash" % (pipes.quote(self.OMNITRUCK))

        command_args = []

        if pre_release or version or download_path:
            command_args += ['-s', '--']

        if pre_release:
            command_args += ['-p']

        if version:
            command_args += ['-v', version]

        if download_path:
            command_args += ['-v', download_path]

        command_args = [pipes.quote(arg) for arg in command_args]
        command_args = ' '.join(command_args)
        command = command + ' ' + command_args

        return command

    def chef_installed(self):
        knife = "/opt/chef/bin/knife"
        command = "test -x %s" % (pipes.quote(knife))
        version = self.options['version']

        if version:
            command += (" && %s --version | grep %s" %
                        (pipes.quote(knife),
                         pipes.quote('Chef: %s' % (version))))

        exit_code = shell.shell_out(command)
        return exit_code == 0

    def install(self):
        return shell.shell_out(self.build_command(**self.options))
