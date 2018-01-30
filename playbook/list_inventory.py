#!/usr/bin/env python

import os
import sys
import json
import yaml

try:
    import configparser as configparser
except:
    import ConfigParser as configparser

HOSTS = configparser.ConfigParser(allow_no_value=True)
HOSTS.optionxform = lambda option: option

def run(INVENTORY):
    if not os.path.exists(INVENTORY):
        print 'Folder do no exists:', INVENTORY
        exit(1)

    fo_servers = []
    try:
        HOSTS.read(os.path.join(INVENTORY, 'hosts'))
        fo_servers = [fo_server for fo_server, _ in HOSTS.items('dev')]
    except Exception as e:
        exit(1)

    for fo_server in fo_servers:
        yaml_file = os.path.join(INVENTORY, 'host_vars' ,
                                 fo_server, 'generated.yaml')
        if not os.path.exists(yaml_file):
            continue
        with open(yaml_file, 'r') as stream:
            ymldata = yaml.load(stream)
            if ymldata is None:
                continue
            clients_list = ymldata['clients']
            for client in clients_list:
                print("{} {}".format(fo_server, client))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        INVENTORY = sys.argv[1]
    else:
        INVENTORY = '../inventory/'
    run(INVENTORY)
