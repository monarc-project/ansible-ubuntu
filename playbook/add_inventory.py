#!/usr/bin/env python
"""
Add an attribute for the ansible inventory
"""

import json
import random
import string
import os
import sys

import sys
import yaml

if len(sys.argv) > 1:
    INVENTORY = sys.argv[1]
else:
    INVENTORY = './inventory/'

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

        path = os.path.join(os.path.abspath(INVENTORY), 'host_vars/',
                                                            newdata['server'])
        if not os.path.exists(path):
            os.makedirs(path)

        generated_file = os.path.join(path, 'generated.yaml')
        with open(generated_file, 'a+') as stream:
            try:
                ymldata = yaml.load(stream)
                if ymldata == None:
                    ymldata = {}
                    ymldata['clients'] = {}
                client_list = ymldata['clients']
                client_name = newdata['proxy_alias']
                client_list[client_name] = {}
                client_list[client_name]['name'] = client_name
                client_list[client_name]['mysql_password'] = get_rnd_string(16)
                client_list[client_name]['salt'] = get_rnd_string(64)
                client_list[client_name]['sql_bootstrap'] = newdata['sql_bootstrap']
                yaml.dump(ymldata, stream)
            except yaml.YAMLError as exc:
                print exc
                exit(1)

run()
