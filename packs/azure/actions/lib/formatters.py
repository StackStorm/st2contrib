__all__ = [
    'to_node_dict'
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
