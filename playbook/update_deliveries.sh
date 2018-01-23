#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

DELIVERIES_DIR="/var/lib/monarc/bo/MonarcAppBO/data/monarc/models/"
DELIVERIES_TEMP_DIR="/tmp/deliveries/"

mkdir $DELIVERIES_TEMP_DIR

FO=$1
CLIENT_NAME=$2
BO=$3

rsync -az $BO:$DELIVERIES_DIR $DELIVERIES_TEMP_DIR

rsync -avz --no-perms --no-owner --no-group --omit-dir-times $DELIVERIES_TEMP_DIR $FO:/var/www/$CLIENT_NAME/deliveries/cases/
