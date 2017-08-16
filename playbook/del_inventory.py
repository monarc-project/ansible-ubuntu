#!/usr/bin/env python
"""
Delete an attribute from the ansible inventory
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
    INVENTORY = '/var/lib/ansible/inventory'

def run():
    """ Main function """
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        exit(1)

    stdin = sys.stdin.read()

    if stdin:
        newdata = json.loads(stdin)

        with open('%s/host_vars/%s/generated.yaml' % (INVENTORY, newdata['server']),
                  'r+') as stream:
            try:
                ymldata = yaml.load(stream)
                client_list = ymldata['clients']
                client_name = newdata['client']
                del client_list[client_name]

                yaml.dump(ymldata)
            except yaml.YAMLError as exc:
                print exc
                exit(1)

run()
