import json
import httplib
import requests
import six
from six.moves.urllib.parse import urljoin

from st2actions.runners.pythonrunner import Action

__all__ = [
    'PostResultAction'
]


def _serialize(data):
    if isinstance(data, dict):
        return '\n'.join(['%s : %s' % (k, v) for k, v in six.iteritems(data)])
    return data


def format_possible_failure_result(result):
    '''
    Error result as generator by the runner container is of the form
    {'message': x, 'traceback': traceback}

    Try and pull out these value upfront. Some other runners that could publish
    these properties would get them for free.
    '''
    output = {}
    message = result.get('message', None)
    if message:
        output['message'] = message
    traceback = result.get('traceback', None)
    if traceback:
        output['traceback'] = traceback
    return output


def format_default_result(result):
    try:
        output = json.loads(result) if isinstance(result, six.string_types) else result
        return _serialize(output)
    except (ValueError, TypeError):
        return result


def format_localrunner_result(result, do_serialize=True):
    output = format_possible_failure_result(result)
    # Add in various properties if they have values
    stdout = result.get('stdout', None)
    if stdout:
        try:
            output['stdout'] = stdout.strip()
        except AttributeError:
            output['stdout'] = stdout
    stderr = result.get('stderr', None)
    if stderr:
        output['stderr'] = stderr.strip()
    return_code = result.get('return_code', 0)
    if return_code != 0:
        output['return_code'] = return_code
    error = result.get('error', None)
    if error:
        output['error'] = error

    return _serialize(output) if do_serialize else output


def format_remoterunner_result(result):
    output = format_possible_failure_result(result)
    output.update({k: format_localrunner_result(v, do_serialize=False)
                   for k, v in six.iteritems(result)})
    return _serialize(output)


def format_actionchain_result(result):
    output = format_possible_failure_result(result)
    return '' if not output else _serialize(output)


def format_mistral_result(result):
    return format_default_result(result)


def format_pythonrunner_result(result):
    output = format_possible_failure_result(result)
    # Add in various properties if they have values
    result_ = result.get('result', None)
    if result_ is not None:
        output['result'] = result_
    stdout = result.get('stdout', None)
    if stdout:
        try:
            output['stdout'] = stdout.strip()
        except AttributeError:
            output['stdout'] = stdout
    stderr = result.get('stderr', None)
    if stderr:
        output['stderr'] = stderr.strip()
    exit_code = result.get('exit_code', 0)
    if exit_code != 0:
        output['exit_code'] = exit_code
    return _serialize(output)


def format_httprunner_result(result):
    return format_default_result(result)


def format_windowsrunner_result(result):
    # same format as pythonrunner
    return format_pythonrunner_result(result)


FORMATTERS = {
    # localrunner
    'local-shell-cmd': format_localrunner_result,
    'run-local': format_localrunner_result,
    'local-shell-script': format_localrunner_result,
    'run-local-script': format_localrunner_result,
    # remoterunner
    'remote-shell-cmd': format_remoterunner_result,
    'run-remote': format_remoterunner_result,
    'remote-shell-script': format_remoterunner_result,
    'run-remote-script': format_remoterunner_result,
    # httprunner
    'http-request': format_httprunner_result,
    'http-runner': format_httprunner_result,
    # mistralrunner
    'mistral-v1': format_mistral_result,
    'mistral-v2': format_mistral_result,
    # actionchainrunner
    'action-chain': format_actionchain_result,
    # pythonrunner
    'run-python': format_pythonrunner_result,
    'python-script': format_pythonrunner_result,
    # windowsrunner
    'windows-cmd': format_windowsrunner_result,
    'windows-script': format_windowsrunner_result
}


class PostResultAction(Action):
    def run(self, result, channel, user=None, whisper=False):
        endpoint = self.config['endpoint']

        if not endpoint:
            raise ValueError('Missing "endpoint" config option')

        url = urljoin(endpoint, "/hubot/st2")

        headers = {}
        headers['Content-Type'] = 'application/json'
        body = {
            'channel': channel,
            'message': self._get_message(result)
        }

        if user:
            body['user'] = user

        if whisper is True:
            body['whisper'] = whisper

        data = json.dumps(body)
        self.logger.info(data)
        response = requests.post(url=url, headers=headers, data=data)

        if response.status_code == httplib.OK:
            self.logger.info('Message successfully posted')
        else:
            self.logger.exception('Failed to post message: %s' % (response.text))
        return True

    def _get_message(self, data):
        envelope = '{message}\nstatus : {status}\nexecution: {execution_id}'.format(**data)
        result = self._get_result(data)
        if result:
            message = '%s\n\nresult :\n--------\n%s' % (envelope, self._get_result(data))
        else:
            message = envelope
        return message

    def _get_result(self, data):
        result = data.get('data', {'result': {}}).get('result', '{}')
        try:
            result = json.loads(result)
        except ValueError:
            # if json.loads fails then very return result as-is. Should not happen.
            return result
        return FORMATTERS.get(data['runner_ref'], format_default_result)(result)
