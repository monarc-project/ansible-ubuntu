#!/usr/bin/env python
"""
Add an attribute for the ansible inventory.
"""

import os
import sys
import json
import random
import string

import yaml

if len(sys.argv) > 1:
    INVENTORY = sys.argv[1]
else:
    INVENTORY = './inventory/'


def get_rnd_string(length):
    """Get random string"""
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(length))


def run():
    """ Main function """
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        return 1

    stdin = sys.stdin.read()

    if stdin:
        try:
            newdata = json.loads(stdin)
        except ValueError:
            return 1

        for new_client in newdata:

            path = os.path.join(os.path.abspath(INVENTORY),
                                'host_vars/',
                                new_client['server'])
            if not os.path.exists(path):
                os.makedirs(path)

            generated_file = os.path.join(path, 'generated.yaml')

            with open(generated_file, 'a+') as stream:
                ymldata = yaml.load(stream)
                if ymldata is None:
                    ymldata = {}
                    ymldata['clients'] = {}

            client_list = ymldata['clients']
            client_name = new_client['proxy_alias']
            client_list[client_name] = {}
            client_list[client_name]['name'] = client_name
            client_list[client_name]['mysql_password'] = get_rnd_string(16)
            client_list[client_name]['salt'] = get_rnd_string(64)
            client_list[client_name]['sql_bootstrap'] = new_client['sql_bootstrap']

            with open(generated_file, 'w') as stream:
                try:
                    yaml.dump(ymldata, stream)
                except yaml.YAMLError as exc:
                    print exc
        else:
            return 1
        return 0
    else:
        return 1


if __name__ == '__main__':
    result = run()
    print(result)
