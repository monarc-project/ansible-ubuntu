#!/bin/sh

spool_dir="/home/cedric/git/MONARC/ansible-ubuntu/playbook/create/"

if [ -z "$(ls -A $spool_dir)" ]; then
   echo ""
else
   cat $spool_dir*.json | jq -s '.' $spool_dir*.json
   #mv $spool_dir*.json /var/tmp/monarc/created/
fi
