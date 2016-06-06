from winrm.protocol import Protocol

from st2actions.runners.pythonrunner import Action

__all__ = [
    'WinRMCmdAction'
]


class WinRMCmdAction(Action):
    def run(self, host, password, command, params, username='Administrator',
            port=5732, secure=True):
        proto = 'https' if secure else 'http'
        p = Protocol(
                endpoint='%s://%s:%i/wsman' % (proto, host, port),  # RFC 2732?
                transport='ntlm',
                username=username,
                password=password,
                server_cert_validation='ignore')
        shell_id = p.open_shell()
        std_out_logs = []
        std_err_logs = []

        # run the command
        command_id = p.run_command(shell_id, command, params)
        std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
        std_out_logs.append(std_out)
        std_err_logs.append(std_err)
        p.cleanup_command(shell_id, command_id)

        p.close_shell(shell_id)
        return std_out_logs, std_err_logs
