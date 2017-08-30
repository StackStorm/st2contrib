from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'CreateJiraIssueAction'
]


class CreateJiraIssueAction(BaseJiraAction):

    def run(self, summary, type, description=None,
            project=None, extra_fields=None):
        project = project or self.config['project']
        data = {
            'project': {'key': project},
            'summary': summary,
            'issuetype': {'name': type}
        }

        if description:
            data['description'] = description

        if extra_fields:
            data.update(extra_fields)

        issue = self._client.create_issue(fields=data)
        result = to_issue_dict(issue)
        return result
