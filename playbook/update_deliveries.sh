#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

DELIVERIES_DIR="/var/lib/monarc/bo/MonarcAppBO/data/monarc/models/"
DELIVERIES_TEMP_DIR="/tmp/deliveries/"

mkdir $DELIVERIES_TEMP_DIR

BO_ADDRESS=$1
FO_ADDRESS=$2
CLIENT_NAME=$3

rsync -az $BO_ADDRESS:$DELIVERIES_DIR $DELIVERIES_TEMP_DIR

rsync -avz --no-perms --no-owner --no-group --omit-dir-times $DELIVERIES_TEMP_DIR $FO_ADDRESS:/var/www/$CLIENT_NAME/deliveries/cases/
