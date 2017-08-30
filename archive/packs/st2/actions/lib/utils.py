def filter_none_values(value):
    """
    Filter out string "None" values from the provided dict.

    :rtype: ``dict``
    """
    result = dict([(k, v) for k, v in value.items() if v != "None"])
    return result
