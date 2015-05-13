from st2actions.runners.pythonrunner import Action

__all__ = [
    'St2ChatOpsFormatExecutionsGetResult'
]


class St2ChatOpsFormatExecutionsGetResult(Action):
    def run(self, result):
        if not result:
            return 'Execution not found.'

        lines = []
        lines.append('ID: %s' % (result['id']))
        lines.append('Action: %s' % (result['action']['ref']))
        lines.append('Status: %s' % (result['status']))
        lines.append('Result: %s' % (result['result']))

        result = '\n'.join(lines)
        return result
