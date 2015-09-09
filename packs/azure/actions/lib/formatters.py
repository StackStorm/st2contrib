__all__ = [
    'to_node_dict',
    'to_container_dict',
    'to_object_dict'
]


def to_node_dict(node):
    result = {
        'id': node.id,
        'name': node.name,
        'state': node.state,
        'public_ips': node.public_ips,
        'private_ips': node.private_ips,
        'extra': node.extra or {}
    }

    return result


def to_container_dict(container):
    result = {
        'name': container.name,
        'extra': container.extra
    }

    return result


def to_object_dict(obj):
    result = {
        'name': obj.name,
        'container_name': obj.container.name,
        'size': obj.size,
        'meta_data': obj.meta_data,
        'extra': obj.extra
    }
    return result
