def format_client_list_result(result):
    """
    Format an API client list return which contains a list of objects.

    :rtype: ``list`` of ``dict``
    """
    formatted = []

    for item in result:
        value = item.to_dict()
        formatted.append(value)

    return formatted
