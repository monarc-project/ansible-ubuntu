#!/bin/sh

set -eu

spool_dir="/var/lib/monarc/bo/MonarcAppBO/data/json/create/"
created_dir="/var/tmp/monarc/created/"
mkdir -p "$created_dir"

if [ ! -d "$spool_dir" -o -z "$(ls -A $spool_dir 2>/dev/null)" ]; then
  echo "[]" # empty JSON array
else
  cat $spool_dir*.json | jq -s '.' $spool_dir*.json
  mv $spool_dir*.json "$created_dir"
fi
