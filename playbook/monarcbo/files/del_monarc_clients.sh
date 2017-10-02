#!/bin/sh

spool_dir="/var/lib/monarc/bo/MonarcAppBO/data/json/delete/"

cat "$spool_dir"*.json
mv "$spool_dir"*.json /var/tmp/monarc/deleted/

# if [ "$(ls -A $spool_dir)" ] ; then
# 	for file in "$spool_dir"/* ; do
# 		cat "$file"
# 		mv "$file" /var/tmp/monarc/deleted/
# 	done
# fi
