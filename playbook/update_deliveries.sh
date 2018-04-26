#!/usr/bin/env bash

if [ ! $# -eq 3 ]
  then
    echo "Three arguments are required. Usage:"
    echo "./update_deliveries.sh BO_ADDRESS FO_ADDRESS CLIENT_NAME"
    exit 1
fi

DELIVERIES_DIR="/var/lib/monarc/bo/MonarcAppBO/data/monarc/models/"
DELIVERIES_TEMP_DIR="/tmp/deliveries/"

if [ ! -d "$DELIVERIES_TEMP_DIR" ]; then
    mkdir $DELIVERIES_TEMP_DIR
fi

BO_ADDRESS=$1
FO_ADDRESS=$2
CLIENT_NAME=$3

# Retrieve the deliveries templates from the back office.
rsync -az $BO_ADDRESS:$DELIVERIES_DIR $DELIVERIES_TEMP_DIR > /dev/null

# Rename the files appropriately for the front offices
find $DELIVERIES_TEMP_DIR -type f -name "*_*" -exec bash -c 'f="$1"; g="${f/*_/}"; mv -- "$f" "$g"' _ '{}' \;

if [ ! $? -eq 0 ]
    then
      echo 'Failed to retrieve deliveries templates from the back office.'
      exit 1
fi

# Update the deliveries templates of the clients
rsync -avz --no-perms --no-owner --no-group --omit-dir-times $DELIVERIES_TEMP_DIR $FO_ADDRESS:/var/www/$CLIENT_NAME/data/monarc/models/ > /dev/null
