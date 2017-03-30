#!/bin/sh

for file in /var/spool/monarc/created/* ; do
	cat "$file"
	mv "$file" /var/tmp/monarc/created/
done
