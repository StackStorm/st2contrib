from lib.base import BaseJiraAction

__all__ = [
    'TransitionJiraIssueAction'
]


class TransitionJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, transition):
        result = self._client.transition_issue(issue_key, transition)
        return result
