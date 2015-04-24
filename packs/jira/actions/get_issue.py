from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'GetJiraIssueAction'
]


class GetJiraIssueAction(BaseJiraAction):
    def run(self, issue_key):
        issue = self._client.issue(issue_key)
        result = to_issue_dict(issue=issue)
        return result
