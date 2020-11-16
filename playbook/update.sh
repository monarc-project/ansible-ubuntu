#!/bin/bash

# Launch the ansible playbook when necessary.
# Launch this file with cron (as the user 'ansible')

if [ ! $# -eq 3 ]
  then
    echo "Three arguments are required. Usage:"
    echo "./update.sh PLAYBOOK_PATH BO_ADDRESS ANSIBLE_PATH"
    exit 1
fi

PLAYBOOK_PATH=$1
BO_ADDRESS=$2
ANSIBLE_PATH=$3

cd $PLAYBOOK_PATH

echo "Executes ansible inventory migrations..."
# backup the inventory (only one backup per day)
tar cfz ../inventory/$(date +%Y-%m-%d)-backup-inventory.tar.gz ../inventory/host_vars
# executes the migrations
../inventory/migrations/001-add_stats_token_to_inventory.py ../inventory

echo "Updating ansible inventory..."
ssh ansible@$BO_ADDRESS sudo -u www-data /usr/local/bin/new_monarc_clients.sh | ./add_inventory.py ../inventory/
ssh ansible@$BO_ADDRESS sudo -u www-data /usr/local/bin/del_monarc_clients.sh | ./del_inventory.py ../inventory/

echo "Running ansible..."
$ANSIBLE_PATH -i ../inventory/ monarc.yaml --user ansible

echo "Synchronizing templates of deliveries..."
./list_inventory.py ../inventory/ | xargs -n2  ./update_deliveries.sh $BO_ADDRESS
