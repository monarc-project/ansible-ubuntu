#!/usr/bin/env bash

DELIVERIES_DIR="/var/lib/monarc/bo/MonarcAppBO/data/monarc/models/*"
DELIVERIES_TEMP_DIR="/tmp/deliveries/"

mkdir $DELIVERIES_TEMP_DIR

SERVER=$1
CLIENT_NAME=$2
BO=$3

rsync -az $BO:$DELIVERIES_DIR $DELIVERIES_TEMP_DIR

rsync -az $DELIVERIES_TEMP_DIR $SERVER:/var/www/$CLIENT_NAME/deliveries/
