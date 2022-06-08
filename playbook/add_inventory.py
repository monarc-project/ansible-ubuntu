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
            newdata = json.loads(stdin)
        except ValueError:
            print("error reading JSON content", file=sys.stderr)
            exit(1)

        for new_client in newdata:
            new_client_name = new_client["proxy_alias"]

            path = os.path.join(
                os.path.abspath(INVENTORY), "host_vars/", new_client["server"]
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

            if new_client_name in ymldata["clients"]:
                continue

            # Add a the new client
            client_list = {}
            client_list["clients"] = ymldata["clients"]
            client_list["clients"][new_client_name] = {}
            client_list["clients"][new_client_name]["name"] = new_client_name
            client_list["clients"][new_client_name]["statsToken"] = secrets.token_urlsafe(64)
            client_list["clients"][new_client_name]["mysql_password"] = get_rnd_string(16)
            client_list["clients"][new_client_name]["salt"] = get_rnd_string(64)
            client_list["clients"][new_client_name]["sql_bootstrap"] = new_client["sql_bootstrap"]

            # Update
            ymldata.update(client_list)

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
