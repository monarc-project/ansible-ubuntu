#!/bin/sh

spool_dir="/var/lib/monarc/bo/MonarcAppBO/data/json/create/"

if [ -z "$(ls -A $spool_dir)" ]; then
   echo ""
else
   echo `jq -s '.' $spool_dir*.json`
   mv $spool_dir*.json /var/tmp/monarc/created/
fi
