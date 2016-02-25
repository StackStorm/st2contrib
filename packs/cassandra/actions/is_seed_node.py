#!/usr/bin/env python2.7

import argparse
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write('Script requires pyyaml to be installed. ' +
                     '``pip install pyyaml``')
    raise


def is_seed_node(node_id, config_file):
    if not os.path.exists(config_file):
        msg = 'Config file %s not found.' % config_file
        sys.stderr.write(msg)
        raise Exception(msg)

    if os.access(config_file, os.R_OK):
        all_seeds = []
        with open(config_file) as f:
            conf = yaml.safe_load(f)
            seed_providers = conf['seed_provider']

            for seed_provider in seed_providers:
                params = seed_provider.get('parameters', None)
                if params:
                    for param in params:
                        seeds = param.get('seeds', None)
                        if seeds:
                            all_seeds.append(seeds)
        return node_id in all_seeds
    else:
        msg = 'No permissions to read config file: %s.' % config_file
        sys.stderr.write(msg)
        raise Exception(msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cassandra config parser.')
    parser.add_argument('--config-file', '-f', required=True,
                        help='Path to cassandra config file.'),
    parser.add_argument('--ip', '--node_id', required=True,
                        help='IP or hostname of host to check.')
    args = parser.parse_args()

    print(str(is_seed_node(args.ip, args.config_file)))
