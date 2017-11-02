#!/bin/sh

spool_dir="/var/lib/monarc/bo/MonarcAppBO/data/json/delete/"

if [ -z "$(ls -A $spool_dir)" ]; then
   echo ""
else
   echo `jq -s '.' $spool_dir*.json`
   mv $spool_dir*.json /var/tmp/monarc/deleted/
fi
