import elasticsearch
import curator
import sys
import logging
from curator.api.utils import get_version, is_master_node

# Elasticsearch versions supported
version_max  = (2, 0, 0)
version_min = (1, 0, 0)
logger = logging.getLogger(__name__)

ES_ARGS = ['host', 'url_prefix', 'port', 'http_auth', 'use_ssl']


def check_version(client):
    """
    Verify version is within acceptable range.  Exit with error if it is not.
    :arg client: The Elasticsearch client connection
    """
    version_number = get_version(client)
    logger.debug('Detected Elasticsearch version {0}'.format(".".join(map(str,version_number))))
    if version_number >= version_max or version_number < version_min:
        print 'Expected Elasticsearch version range > {0} < {1}'.format(".".join(map(str,version_min)),".".join(map(str,version_max)))
        print 'ERROR: Incompatible with version {0} of Elasticsearch.  Exiting.'.format(".".join(map(str,version_number)))
        sys.exit(1)


def check_master(client, master_only=False):
    """
    Check if master node.  If not, exit with error code
    """
    if master_only and not is_master_node(client):
        logger.info('Master-only flag detected. Connected to non-master node. Aborting.')
        sys.exit(9)


def get_client(**kwargs):
    """
    Return an Elasticsearch client using the provided parameters
    """
    kwargs = {k:kwargs[k] for k in ES_ARGS if kwargs[k]}
    kwargs['master_only'] = False if not 'master_only' in kwargs else kwargs['master_only']
    logger.debug("kwargs = {0}".format(kwargs))
    master_only = kwargs.pop('master_only')
    try:
        client = elasticsearch.Elasticsearch(**kwargs)
        # Verify the version is acceptable.
        check_version(client)
        # Verify "master_only" status, if applicable
        check_master(client, master_only=master_only)
        return client
    except Exception as e:
        print "ERROR: Connection failure: {0}".format(e.message)
        sys.exit(1)


def compact_dict(source_dict):
    """
    Drop all elements equal to None
    """
    return {k:v for k,v in source_dict.items() if v is not None}


def xstr(s):
    """
    IdiotOmatic xstr.
    """
    return '' if s is None else str(s)
