#!/bin/bash

# Launch the ansible playbook when necessary.
# Launch this file with cron (as the user 'ansible')

if [ $# -lt 3 ]
  then
    echo "Three arguments are required. Usage:"
    echo "./update-clients.sh PLAYBOOK_PATH BO_ADDRESS ANSIBLE_PATH [PYTHON_PATH]"
    exit 1
fi

# python is sneaky
export PYTHONUNBUFFERED=1

PLAYBOOK_PATH=$1
BO_ADDRESS=$2
ANSIBLE_PATH=$3

if [ $# -eq 4 ]
  then
    PYTHON_PATH=$4
  else
    PYTHON_PATH=`which python`
fi

cd $PLAYBOOK_PATH

echo "Executes ansible inventory migrations..."
# backup the inventory (only one backup per day)
#tar cfz ../inventory/$(date +%Y-%m-%d)-backup-inventory.tar.gz ../inventory/host_vars

echo "Updating ansible inventory..."
ssh ansible@$BO_ADDRESS sudo -u www-data /usr/local/bin/update_monarc_clients.sh | $PYTHON_PATH ./update_inventory.py ../inventory/

echo "Running ansible..."
$ANSIBLE_PATH --diff -i ../inventory/ update_clients.yaml --user ansible

echo "Clean up the inventory, remove sql_update"
find ../inventory/host_vars -type f -name 'generated.yaml' -exec sed -i '/sql_update/d' {} +
