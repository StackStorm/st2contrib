__all__ = [
    'issue_to_dict'
]


def issue_to_dict(issue):
    result = {}

    if issue.closed_by:
        closed_by = issue.closed_by.name
    else:
        closed_by = None

    result['id'] = issue.id
    result['repository'] = issue.repository.name
    result['title'] = issue.title
    result['body'] = issue.body
    result['url'] = issue.html_url
    result['state'] = issue.state
    result['labels'] = issue.labels
    result['created_at'] = issue.created_at
    result['closed_at'] = issue.closed_at
    result['closed_by'] = closed_by
    return result
