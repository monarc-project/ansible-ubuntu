#!/usr/bin/env python
"""
Delete an attribute from the ansible inventory
"""

import json
import random
import string

import sys
import yaml

INVENTORY = '/var/lib/ansible/inventory'

def run():
    """ Main function """
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
