from pywinexe.api import cmd as run_cmd

from st2actions.runners.pythonrunner import Action

__all__ = [
    'SetupWinRMAction'
]


class SetupWinRMAction(Action):
    def run(self, host, password, username='Administrator'):
        """
        Setup WinRM on a remote node to accept non-cert trusted connections
        """
        out = run_cmd(
            'echo hello',
            args=[],
            user=username,
            password=password,
            host=host)
        cmds = [
            "winrm quickconfig -quiet",
            "winrm set winrm/config/service/auth @{Basic=\"true\"}",
            "winrm set winrm/config/service @{AllowUnencrypted=\"true\"}"
        ]
        out = [
            run_cmd(
                cmd,
                args=[],
                user=username,
                password=password,
                host=host) for cmd in cmds]
        return {'stdout': out}
