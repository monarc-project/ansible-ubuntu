#!/usr/bin/env python

import os
import glob
import sys
import yaml

def run(INVENTORY, BO):
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        exit(1)

    yamls = os.path.join(INVENTORY, 'host_vars' ,'*', 'generated.yaml')

    for generated_file in glob.glob(yamls):
        server_name = os.path.dirname(os.path.relpath("../inventory/host_vars/FO/generated.yaml", os.path.join(INVENTORY, 'host_vars')))
        with open(generated_file, 'r') as stream:
            ymldata = yaml.load(stream)
            if ymldata is None:
                continue
            clients_list = ymldata['clients']
            for client in clients_list:
                print("{} {} {}".format(server_name, client, BO))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        INVENTORY = sys.argv[1]
        BO = sys.argv[2].strip()
    else:
        INVENTORY = './inventory/'
        BO = 'BO'
    run(INVENTORY, BO)
