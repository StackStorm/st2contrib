__all__ = [
    'google_result_to_dict'
]


def google_result_to_dict(obj):
    result = {
        'name': obj.name,
        'description': obj.description,
        'link': obj.link,
        'google_link': obj.google_link,
        'thumb': obj.thumb
    }

    return result
