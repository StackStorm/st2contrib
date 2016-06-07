from pywinexe.api import cmd as run_cmd

from st2actions.runners.pythonrunner import Action

__all__ = [
    'LockdownWinRMAction'
]


class LockdownWinRMAction(Action):
    def run(self, host, password, username='Administrator'):
        """
        Setup WinRM on a remote node
        """
        cmds = [
            "winrm set winrm/config/service/auth @{Basic=\"false\"}",
            "winrm set winrm/config/service @{AllowUnencrypted=\"false\"}"
        ]
        out = [
            run_cmd(
                cmd,
                args=[],
                user=username,
                password=password,
                host=host) for cmd in cmds]
        return {'stdout': out}
