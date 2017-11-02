#!/bin/bash

# Launch the ansible playbook when necessary.
# Launch this file with cron (as the user 'ansible')

PLAYBOOK_PATH=$1
BO=$2
ANSIBLE_PATH=$3

cd $PLAYBOOK_PATH

ssh ansible@$BO sudo -u www-data /usr/local/bin/new_monarc_clients.sh | ./add_inventory.py ../inventory/

ssh ansible@$BO sudo -u www-data /usr/local/bin/del_monarc_clients.sh | ./del_inventory.py ../inventory/

$ANSIBLE_PATH -i ../inventory/ monarc.yaml --user ansible
