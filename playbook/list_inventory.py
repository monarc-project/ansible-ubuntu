#!/usr/bin/env python

import os
import glob
import sys
import json
import yaml
from pathlib import Path
from subprocess import call

def run(INVENTORY, BO):
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        exit(1)

    INVENTORY = os.path.join(INVENTORY, 'host_vars' ,'*', 'generated.yaml')

    for generated_file in glob.glob(INVENTORY):
        server_name = Path(generated_file).parts[-2]
        with open(generated_file, 'r') as stream:
            ymldata = yaml.load(stream)
            if ymldata is None:
                continue
            clients_list = ymldata['clients']
            for client in clients_list:
                try:
                    # call(['./update_deliveries.sh', server_name, client, BO])
                    print("{} {} {}".format(server_name, client, BO))
                except:
                    continue


if __name__ == '__main__':
    if len(sys.argv) > 2:
        INVENTORY = sys.argv[1]
        BO = sys.argv[2]
    else:
        INVENTORY = './inventory/'
        BO = 'BO'
    run(INVENTORY, BO)
