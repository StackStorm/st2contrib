# pylint: disable=no-member

import elasticsearch
import sys
import logging
from curator.api.utils import get_version, is_master_node

# Elasticsearch versions supported
version_max = (2, 2, 0)
version_min = (1, 0, 0)
logger = logging.getLogger(__name__)


def check_version(client):
    """
    Verify version is within acceptable range.  Exit with error if it is not.
    :arg client: The Elasticsearch client connection
    """
    version_number = get_version(client)
    logger.debug('Detected Elasticsearch version %s', ".".join(map(str, version_number)))
    if version_number >= version_max or version_number < version_min:
        vmin = ".".join(map(str, version_min))
        vmax = ".".join(map(str, version_max))
        vnum = ".".join(map(str, version_number))
        print 'Expected Elasticsearch version range > {} < {}'.format(vmin, vmax)
        print 'ERROR: Incompatible with version {} of Elasticsearch.  Exiting.'.format(vnum)
        sys.exit(1)


def check_master(client, master_only=False):
    """
    Check if master node.  If not, exit with error code
    """
    if master_only and not is_master_node(client):
        logger.info('Master-only flag detected. Connected to non-master node. Aborting.')
        sys.exit(9)


def chunk_index_list(indices):
    """
    This utility chunks very large index lists into 3KB chunks
    It measures the size as a csv string, then converts back into a list
    for the return value.
    :arg indices: A list of indices to act on.

    !When version > 3.0.3 of curator is released. Should be removed!
    """
    chunks = []
    chunk = ""
    for index in indices:
        if len(chunk) < 3072:
            if not chunk:
                chunk = index
            else:
                chunk += "," + index
        else:
            chunks.append(chunk.split(','))
            chunk = index
    chunks.append(chunk.split(','))
    return chunks


def get_client(host, port=9200, url_prefix=None, http_auth=None, use_ssl=False,
               master_only=False, timeout=30):
    """
    Return an Elasticsearch client using the provided parameters
    """
    kwargs = compact_dict({
        'host': host, 'port': port, 'http_auth': http_auth,
        'url_prefix': url_prefix, 'use_ssl': use_ssl,
        'timeout': timeout
    })
    logger.debug("ES client kwargs = %s", kwargs)
    try:
        client = elasticsearch.Elasticsearch(**kwargs)
        # Verify the version is acceptable.
        check_version(client)
        # Verify "master_only" status, if applicable
        check_master(client, master_only=master_only)
        return client
    except Exception as e:  # noqa
        print "ERROR: Connection failure: {0}".format(e.message)
        sys.exit(1)


def compact_dict(source_dict):
    """
    Drop all elements equal to None
    """
    return {k: v for k, v in source_dict.items() if v is not None}


def xstr(s):
    """
    IdiotOmatic xstr.
    """
    return '' if s is None else str(s)
