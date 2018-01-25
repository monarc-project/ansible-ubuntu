#!/usr/bin/env python

import os
import glob
import sys
import json
import yaml

def run(INVENTORY):
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        exit(1)

    yamls = os.path.join(INVENTORY, 'host_vars' ,'*', 'generated.yaml')

    for generated_file in glob.glob(yamls):
        server_name = os.path.dirname(
                os.path.relpath("../inventory/host_vars/FO/generated.yaml",
                                os.path.join(INVENTORY, 'host_vars')))
        with open(generated_file, 'r') as stream:
            ymldata = yaml.load(stream)
            if ymldata is None:
                continue
            clients_list = ymldata['clients']
            for client in clients_list:
                print("{} {}".format(server_name, client))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        INVENTORY = sys.argv[1]
    else:
        INVENTORY = '../inventory/'
    run(INVENTORY)
