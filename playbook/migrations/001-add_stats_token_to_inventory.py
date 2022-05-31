#!/usr/bin/env python3

import os
import sys
import json
import yaml
import secrets

try:
    import configparser as configparser
except:
    import ConfigParser as configparser

HOSTS = configparser.ConfigParser(allow_no_value=True)
HOSTS.optionxform = lambda option: option


def run(INVENTORY):
    """Update the inventory with the 'apiKey' = {statsToken}."""
    if not os.path.exists(INVENTORY):
        print("Folder do no exists: {}".format(INVENTORY))
        exit(1)

    fo_servers = []
    try:
        HOSTS.read(os.path.join(INVENTORY, "hosts"))
        fo_servers = [fo_server for fo_server, _ in HOSTS.items("dev")]
    except Exception as e:
        exit(1)

    for fo_server in fo_servers:
        # iterate through each yaml configuration files of the FO servers
        yaml_file = os.path.join(INVENTORY, "host_vars", fo_server, "generated.yaml")
        if not os.path.exists(yaml_file):
            continue
        with open(yaml_file, "r") as stream:
            ymldata = yaml.load(stream, Loader=yaml.FullLoader)
            if ymldata is None:
                continue
            for client in ymldata["clients"]:
                # update the client section if needed
                if "statsToken" not in ymldata["clients"][client]:
                    ymldata["clients"][client]["statsToken"] = secrets.token_urlsafe(64)
            # save the yaml configuration file
            with open(yaml_file, "w") as stream:
                try:
                    yaml.dump(ymldata, stream)
                except yaml.YAMLError as exc:
                    print(exc)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        INVENTORY = sys.argv[1]
    else:
        INVENTORY = "../inventory/"
    run(INVENTORY)
