#!/bin/bash

# Launch the ansible playbook when necessary.
# Launch this file with cron (as the user 'ansible')

if [ ! $# -eq 3 ]
  then
    echo "Three arguments are required. Usage:"
    echo "./update.sh PLAYBOOK_PATH BO_ADDRESS ANSIBLE_PATH"
    exit 1
fi

PLAYBOOK_CFG="monarc.yaml"
PLAYBOOK_PATH=$1
BO_ADDRESS=$2
ANSIBLE_PATH=$3

cd $PLAYBOOK_PATH

echo "Updating ansible inventory..."
addition=$(ssh ansible@$BO_ADDRESS sudo -u www-data /usr/local/bin/new_monarc_clients.sh | ./add_inventory.py ../inventory/)
removal=$(ssh ansible@$BO_ADDRESS sudo -u www-data /usr/local/bin/del_monarc_clients.sh | ./del_inventory.py ../inventory/)

echo "Running ansible..."
if [ "$addition" == 0 ] || [ "$removal" == 0 ] ; then
    $ANSIBLE_PATH -i ../inventory/ $PLAYBOOK_CFG --user ansible
else
    $ANSIBLE_PATH -i ../inventory/ $PLAYBOOK_CFG --user ansible --skip-tags "update-clients"
fi

echo "Synchronizing templates of deliveries..."
./list_inventory.py ../inventory/ | xargs -n2  ./update_deliveries.sh $BO_ADDRESS
