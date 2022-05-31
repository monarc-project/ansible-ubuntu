#!/bin/sh

spool_dir="/var/lib/monarc/bo/MonarcAppBO/data/json/delete/"
deleted_dir="/var/tmp/monarc/deleted/"
mkdir -p "$deleted_dir"

if [ ! -d "$spool_dir" -o -z "$(ls -A $spool_dir 2>/dev/null)" ]; then
  echo "[]" # empty JSON array
else
  echo `jq -s '.' $spool_dir*.json`
  mv $spool_dir*.json "$deleted_dir"
fi
