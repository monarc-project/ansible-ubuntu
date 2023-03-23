#!/usr/bin/env python3
"""
Add an attribute for the ansible inventory.
"""

import os
import sys
import json
import random
import string
import secrets

import yaml

if len(sys.argv) > 1:
    INVENTORY = sys.argv[1]
else:
    INVENTORY = "./inventory/"


def get_rnd_string(length):
    """Get random string"""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def run():
    """ Main function """
    if not os.path.exists(INVENTORY):
        print("Folder do no exists: {}".format(INVENTORY))
        exit(1)

    stdin = sys.stdin.read()

    if stdin:
        try:
            update_data = json.loads(stdin)
        except ValueError:
            print("error reading JSON content", file=sys.stderr)
            exit(1)

        for update_client in update_data:
            client_name = update_client["proxy_alias"]

            path = os.path.join(
                os.path.abspath(INVENTORY), "host_vars/", update_client["server"]
            )
            if not os.path.isdir(path):
                os.makedirs(path)

            generated_file = os.path.join(path, "generated.yaml")
            if not os.path.exists(generated_file):
                open(generated_file, 'a').close()

            # Read the yaml file
            with open(generated_file, "r") as stream:
                ymldata = yaml.load(stream, Loader=yaml.FullLoader)
                if ymldata is None:
                    ymldata = {}
                    ymldata["clients"] = {}

            areClientsChanged = False
            if client_name in ymldata["clients"]:
                # Update the client.
                if "isBackgroundProcessActive" in update_client:
                    ymldata["clients"][client_name]
                    ["isBackgroundProcessActive"] = update_client["isBackgroundProcessActive"]
                    areClientsChanged = True
                if "twoFactorAuthEnforced" in update_client:
                    ymldata["clients"][client_name]["twoFactorAuthEnforced"] = update_client["twoFactorAuthEnforced"]
                    areClientsChanged = True

            if areClientsChanged:
                with open(generated_file, "w") as stream:
                    try:
                        yaml.dump(ymldata, stream)
                    except yaml.YAMLError as exc:
                        print(exc)
        else:
            exit(0)
    else:
        print("can't read stdin", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    run()
