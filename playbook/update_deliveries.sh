#!/usr/bin/env bash

set -euo pipefail

if [ ! $# -eq 3 ]
  then
    echo "Three arguments are required. Usage:"
    echo "./update_deliveries.sh BO_ADDRESS FO_ADDRESS CLIENT_NAME"
    exit 1
fi

DELIVERIES_DIR="/var/lib/monarc/bo/MonarcAppBO/deliveries/cases/"
DELIVERIES_MODELS_DIR="/var/lib/monarc/bo/MonarcAppBO/data/monarc/models/"
DELIVERIES_TEMP_DIR=$(mktemp -d /tmp/monarc-deliveries.XXXXXX)

cleanup() {
    rm -rf "$DELIVERIES_TEMP_DIR"
}

trap cleanup EXIT

BO_ADDRESS=$1
FO_ADDRESS=$2
CLIENT_NAME=$3

# Retrieve the default deliveries templates shipped with the BackOffice.
rsync -az "$BO_ADDRESS:$DELIVERIES_DIR" "$DELIVERIES_TEMP_DIR/"

# Overlay BackOffice model templates only when they have the same relative path
# as a default template. Historical uploads with generated file names are skipped.
rsync -az --existing --ignore-times "$BO_ADDRESS:$DELIVERIES_MODELS_DIR" "$DELIVERIES_TEMP_DIR/"

# Update the resolved defaults without deleting client-only templates or
# replacing a newer client-side file.
rsync -az --update --no-perms --no-owner --no-group --omit-dir-times \
    "$DELIVERIES_TEMP_DIR/" "$FO_ADDRESS:/var/www/$CLIENT_NAME/deliveries/cases/"
