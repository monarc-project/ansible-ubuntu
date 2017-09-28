#!/usr/bin/env python
"""
Delete an attribute from the ansible inventory.
"""

import os
import sys
import json
import string

import yaml

if len(sys.argv) > 1:
    INVENTORY = sys.argv[1]
else:
    #INVENTORY = '/var/lib/ansible/inventory'
    INVENTORY = './inventory/'

def run():
    """ Main function """
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        exit(1)

    stdin = sys.stdin.read()

    if stdin:
        newdata = json.loads(stdin)

        path = os.path.join(os.path.abspath(INVENTORY), 'host_vars/',
                                                            newdata['server'])
        if not os.path.exists(path):
            print 'Folder do no exists:', path
            exit(1)

        generated_file = os.path.join(path, 'generated.yaml')

        with open(generated_file, 'a+') as stream:
            ymldata = yaml.load(stream)
            client_list = ymldata['clients']
            client_name = newdata['proxy_alias']
            try:
                del client_list[client_name]
            except:
                exit(1)

        with open(generated_file, 'w') as stream:
            try:
                yaml.dump(ymldata, stream)
                exit(0)
            except yaml.YAMLError as exc:
                print exc
                exit(1)
    else:
        exit(3)

if __name__ == '__main__':
    run()
