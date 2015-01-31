import shellhelpers as shell

class Omnibus(object):
    OMNITRUCK = 'https://www.chef.io/chef/install.sh'

    def __init__(self, options):
        supports = ('pre_release', 'version', 'download_path')
        self.options = { k: options[k] for k in supports }

    def build_command(self, version=None, pre_release=False, download_path=None):
        command = "curl -sL %s | sudo bash" % self.OMNITRUCK

        if pre_release or version != None or download_path != None:
          command += " -s --"

        if pre_release:
          command += " -p"

        if version != None:
          command += " -v \"%s\"" % version

        if download_path:
          command += " -d \"%s\"" % download_path

        return command


    def chef_installed(self):
        knife = "/opt/chef/bin/knife"
        command = "test -x %s" % knife
        version = self.options['version']
        if version != None:
          command += " && %s --version | grep 'Chef: %s'" % (knife, version)

        exit_code = shell.shell_out(command)
        return exit_code == 0


    def install(self):
        return shell.shell_out(self.build_command(**self.options))
