#!/bin/bash

basedir="$(dirname "$(readlink -f $0)")"

masterhost="$(awk -F'"' '$1 == "master=" { print $2}' $basedir/../inventory/hosts)"

set -x
set -e

bash -xe $basedir/update.sh $basedir/ "$masterhost" "$(which ansible-playbook)" "$(which python3)"
