#!/usr/bin/env python

"""
Script which updates README.md with a list of all the available packs.
"""

import os
import copy
import glob
import json
import argparse

import yaml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKS_DIR = os.path.join(CURRENT_DIR, '../packs')
README_PATH = os.path.join(CURRENT_DIR, '../README.md')

PARSER_FUNCS = {
    '.json': json.loads,
    '.yml': yaml.safe_load,
    '.yaml': yaml.safe_load
}

BASE_REPO_URL = 'https://github.com/StackStorm/st2contrib'
BASE_PACKS_URL = 'https://github.com/StackStorm/st2contrib/tree/master/packs'
PACK_ICON_URL = 'https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/%(name)s/icon.png'
NO_PACK_ICON_URL = 'https://raw.githubusercontent.com/StackStorm/st2contrib/master/packs/st2/icon.png'


def get_pack_list():
    packs = os.listdir(PACKS_DIR)
    packs = sorted(packs)
    return packs


def get_pack_metadata(pack):
    metadata_path = os.path.join(PACKS_DIR, pack, 'pack.yaml')
    with open(metadata_path, 'r') as fp:
        content = fp.read()

    metadata = yaml.safe_load(content)

    icon_path = os.path.join(PACKS_DIR, pack, 'icon.png')
    if os.path.exists(icon_path):
        metadata['icon_url'] = PACK_ICON_URL % {'name': pack}
    else:
        metadata['icon_url'] = NO_PACK_ICON_URL

    return metadata


def get_pack_resources(pack):
    sensors_path = os.path.join(PACKS_DIR, pack, 'sensors/')
    actions_path = os.path.join(PACKS_DIR, pack, 'actions/')

    sensor_metadata_files = glob.glob(sensors_path + '/*.json')
    sensor_metadata_files += glob.glob(sensors_path + '/*.yaml')
    sensor_metadata_files += glob.glob(sensors_path + '/*.yml')

    action_metadata_files = glob.glob(actions_path + '/*.json')
    action_metadata_files += glob.glob(actions_path + '/*.yaml')
    action_metadata_files += glob.glob(actions_path + '/*.yml')

    resources = {
        'sensors': [],
        'actions': []
    }

    for sensor_metadata_file in sensor_metadata_files:
        file_name, file_ext = os.path.splitext(sensor_metadata_file)

        with open(sensor_metadata_file, 'r') as fp:
            content = fp.read()

        content = PARSER_FUNCS[file_ext](content)
        item = {
            'name': content['class_name'],
            'description': content.get('description', None)
        }
        resources['sensors'].append(item)

    for action_metadata_file in action_metadata_files:
        file_name, file_ext = os.path.splitext(action_metadata_file)

        with open(action_metadata_file, 'r') as fp:
            content = fp.read()

        content = PARSER_FUNCS[file_ext](content)

        if 'name' not in content:
            continue

        item = {
            'name': content['name'],
            'description': content.get('description', None)
        }
        resources['actions'].append(item)

    resources['sensors'] = sorted(resources['sensors'], key=lambda i: i['name'])
    resources['actions'] = sorted(resources['actions'], key=lambda i: i['name'])

    return resources


def generate_pack_list_table(packs):
    lines = []

    lines.append('Icon | Name | Description | Keywords | Author | Latest Version | Available Resources')
    lines.append('---- | ---- | ----------- | -------- | ------ | -------------- | -------------------')

    for pack_name, metadata in packs:
        values = copy.deepcopy(metadata)
        values['base_packs_url'] = BASE_PACKS_URL
        values['base_repo_url'] = BASE_REPO_URL
        values['keywords'] = ', '.join(metadata.get('keywords', []))
        line = '![%(name)s icon](%(icon_url)s) | [%(name)s](%(base_packs_url)s/%(name)s) | %(description)s | %(keywords)s | [%(author)s](mailto:%(email)s) | %(version)s | [click](%(base_repo_url)s#%(name)s-pack)' % (values)
        lines.append(line)

    result = '\n'.join(lines)
    return result


def generate_pack_resources_tables(packs):
    lines = []

    for pack_name, metadata in packs:
        pack_resources = get_pack_resources(pack=pack_name)
        table = generate_pack_resources_table(pack_name=pack_name,
                                              metadata=metadata,
                                              resources=pack_resources)
        if not table:
            continue

        lines.append(table)

    result = '\n\n'.join(lines)
    return result


def generate_pack_resources_table(pack_name, metadata, resources):
    lines = []

    if not resources['sensors'] and not resources['actions']:
        return None

    lines.append('### ![%s icon](%s) %s pack' % (pack_name, metadata['icon_url'], pack_name))
    lines.append('')

    if resources['sensors']:
        lines.append('#### Sensors')
        lines.append('')
        lines.append('Name | Description')
        lines.append('---- | -----------')

        for sensor in resources['sensors']:
            lines.append('%s | %s' % (sensor['name'], sensor['description']))

        if resources['actions']:
            lines.append('')

    if resources['actions']:
        lines.append('#### Actions')
        lines.append('')
        lines.append('Name | Description')
        lines.append('---- | -----------')

        for action in resources['actions']:
            lines.append('%s | %s' % (action['name'], action['description']))

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

    table1 = generate_pack_list_table(packs=packs_with_metadata)
    table2 = generate_pack_resources_tables(packs=packs_with_metadata)
    table = '%s\n%s' % (table1, table2)
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
