from netaddr import IPAddress

__all__ = [
    'to_server_dict',
    'to_dns_zone_dict',
    'to_dns_record_dict'
]


def to_server_dict(server):
    public_ips = [ip['addr'] for ip in server.addresses['public']]
    private_ips = [ip['addr'] for ip in server.addresses['private']]

    # Pick out first public IPv4 and IPv6 address
    public_ipv4 = None
    public_ipv6 = None

    for ip in public_ips:
        try:
            ip_obj = IPAddress(ip)
        except Exception:
            continue

        if not ip_obj.is_private():
            if ip_obj.version == 4:
                public_ipv4 = ip
            elif ip_obj.version == 6:
                public_ipv6 = ip

    result = {
        'id': server.id,
        'name': server.name,
        'status': server.status,
        'image_id': server.image['id'],
        'flavor_id': server.flavor['id'],
        'public_ips': public_ips,
        'private_ips': private_ips,
        'public_ipv4': public_ipv4,
        'public_ipv6': public_ipv6,
        'key_name': server.key_name,
        'metadata': server.metadata
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


def to_dns_record_dict(record):
    result = {
        'id': record.id,
        'name': record.name,
        'type': record.type,
        'data': record.data,
        'ttl': record.ttl
    }
    return result
