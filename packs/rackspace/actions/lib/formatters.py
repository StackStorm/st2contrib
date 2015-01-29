__all__ = [
    'to_server_dict',
    'to_dns_zone_dict'
]


def to_server_dict(server):
    public_ips = [ip['addr'] for ip in server.addresses['public']]
    private_ips = [ip['addr'] for ip in server.addresses['private']]
    result = {
        'id': server.id,
        'name': server.name,
        'status': server.status,
        'image_id': server.image['id'],
        'flavor_id': server.flavor['id'],
        'public_ips': public_ips,
        'private_ips': private_ips,
        'key_name': server.key_name
    }
    return result


def to_dns_zone_dict(zone):
    result = {
        'id': zone.id,
        'name': zone.name,
        'email_address': zone.emailAddress,
        'ttl': zone.ttl
    }
    return result
