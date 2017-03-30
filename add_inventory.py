#!/usr/bin/env python
"""
Add an attribute for the ansible inventory
"""

import json
import random
import string

import sys
import yaml

INVENTORY = '/var/lib/ansible/inventory/'

#{"server":"client4.prod.dims.lc1.conostix.com","client":"grclux","salt":"zG@0q1EI",
#"jabber_account":"grclux@jabber.cases.lu","sql_bootstrap":

def get_rnd_string(length):
    """Get random string"""
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(length))

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
                client_list[client_name] = {}
                client_list[client_name]['name'] = client_name
                client_list[client_name]['mysql_password'] = get_rnd_string(16)
                client_list[client_name]['salt'] = get_rnd_string(64)

                yaml.dump(ymldata)
            except yaml.YAMLError as exc:
                print exc
                exit(1)

run()
