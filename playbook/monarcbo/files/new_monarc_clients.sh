#!/bin/sh

spool_dir="/var/lib/monarc/bo/MonarcAppBO/data/json/create/"

cat "$spool_dir"*.json
mv "$spool_dir"*.json /var/tmp/monarc/created/

# if [ "$(ls -A $spool_dir)" ] ; then
# 	for file in "$spool_dir"/* ; do
# 		cat "$file"
# 		mv "$file" /var/tmp/monarc/created/
# 	done
# fi
