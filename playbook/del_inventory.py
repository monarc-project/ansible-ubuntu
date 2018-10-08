#!/usr/bin/env python
"""
Delete an attribute from the ansible inventory.
"""

import os
import sys
import json

import yaml

if len(sys.argv) > 1:
    INVENTORY = sys.argv[1]
else:
    INVENTORY = './inventory/'


def run():
    """ Main function """
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        return 1

    stdin = sys.stdin.read()

    if stdin:
        try:
            todelete = json.loads(stdin)
        except ValueError:
            return 1

        for to_delete in todelete:

            path = os.path.join(os.path.abspath(INVENTORY),
                                'host_vars/',
                                to_delete['server'])
            if not os.path.exists(path):
                print 'Folder do no exists:', path
                return 1

            generated_file = os.path.join(path, 'generated.yaml')

            with open(generated_file, 'a+') as stream:
                ymldata = yaml.load(stream)
                client_list = ymldata['clients']
                client_name = to_delete['proxy_alias']
                try:
                    del client_list[client_name]
                except Exception:
                    pass

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
