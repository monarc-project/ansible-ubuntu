#!/bin/sh

spool_dir="/var/spool/monarc/deleted"

if [ "$(ls -A $spool_dir)" ] ; then
	for file in "$spool_dir"/* ; do
		cat "$file"
		mv "$file" /var/tmp/monarc/deleted/
	done
fi
