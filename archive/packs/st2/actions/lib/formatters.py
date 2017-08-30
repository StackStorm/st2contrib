def format_client_list_result(result, exclude_attributes=None):
    """
    Format an API client list return which contains a list of objects.

    :param exclude_attributes: Optional list of attributes to exclude from the item.
    :type exclude_attributes: ``list``

    :rtype: ``list`` of ``dict``
    """
    formatted = []

    for item in result:
        value = item.to_dict(exclude_attributes=exclude_attributes)
        formatted.append(value)

    return formatted
