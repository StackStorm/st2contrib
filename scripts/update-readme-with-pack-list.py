#!/usr/bin/env python

"""
Script which updates README.md with a list of all the available packs.
"""

import os
import copy
import argparse

import yaml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKS_DIR = os.path.join(CURRENT_DIR, '../packs')
README_PATH = os.path.join(CURRENT_DIR, '../README.md')

BASE_URL = 'https://github.com/StackStorm/st2contrib/tree/master/packs'


def get_pack_list():
    packs = os.listdir(PACKS_DIR)
    packs = sorted(packs)
    return packs


def get_pack_metadata(pack):
    metadata_path = os.path.join(PACKS_DIR, pack, 'pack.yaml')
    with open(metadata_path, 'r') as fp:
        content = fp.read()

    metadata = yaml.safe_load(content)
    return metadata


def generate_pack_list_table(packs):
    lines = []

    lines.append('Name | Description | Author | Latest Version')
    lines.append('---- | ----------- | ------ | -------------- ')

    for pack_name, metadata in packs:
        values = copy.deepcopy(metadata)
        values['base_url'] = BASE_URL
        line = '| [%(name)s](%(base_url)s/%(name)s) | %(description)s | %(author)s | %(version)s' % (values)
        lines.append(line)

    result = '\n'.join(lines)
    return result


def get_updated_readme(table):
    with open(README_PATH, 'r') as fp:
        current_readme = fp.read()

    head = current_readme.split('## Available Packs\n\n')[0]
    tail = current_readme.split('## License, and Contributors Agreement')[1]

    replacement = '## Available Packs\n\n'
    replacement += table + '\n\n'
    replacement += '## License, and Contributors Agreement'
    updated_readme = head + replacement + tail
    return updated_readme


def main(dry_run):
    packs = get_pack_list()

    packs_with_metadata = []
    for pack in packs:
        try:
            metadata = get_pack_metadata(pack=pack)
        except IOError:
            continue

        packs_with_metadata.append((pack, metadata))
    table = generate_pack_list_table(packs=packs_with_metadata)
    updated_readme = get_updated_readme(table=table)

    if dry_run:
        print(updated_readme)
    else:
        with open(README_PATH, 'w') as fp:
            fp.write(updated_readme)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dry-run', help='Print the new readme to stdout',
                        action='store_true', default=False)

    args = parser.parse_args()
    main(dry_run=args.dry_run)
