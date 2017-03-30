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

#{"serveur":"client2.prod.dims.lc1.conostix.com","client":"sesluxbg"}

def get_rnd_string(length):
    """Get random string"""
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(length))

def run():
    """ Main function """
    newdata = json.loads(sys.stdin.read())

    if newdata:
        with open('%s/host_vars/%s/generated.yaml' % (INVENTORY, newdata['server']), 'r+') as stream:
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
