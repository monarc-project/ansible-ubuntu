# Ansible playbook for MONARC deployement

This playbook is used to deploy MONARC.


![MONARC architecture](images/monarc-architecture.png "MONARC architecture")


## Requirements

* install Python 2 on all servers;
* ansible must be installed on the configuration server.



## Usage

    $ sudo apt-get install ansible
    $ git clone https://github.com/monarc-project/ansible-ubuntu.git
    $ cd ansible-ubuntu/playbook
    $ ansible-playbook -i ../inventory/ monarc.yaml -u monarc -k -K

*-k -K* forces the SSH authentication by simple password. In this case
*sshpass* must be installed on the configuration server.

However, it is recommended to use a SSH key associated to a user dedicated to
ansible. The *ansible* user must be created on each servers.


### Notes

1. In the file __inventory/hosts__:

* the section *dev* is for the FO;
* the section *master* is for the BO;
* master in the section *dev:vars* is the ip/domain of the BO;
* publicHost in the section *dev:vars* is the ip/domain of the RPX.

2. Add an attribute for the ansible inventory:

    $ ssh monarc@<IP-OF-THE-BO> sudo -u www-data /usr/local/bin/new_monarc_clients.sh | ./ansible-ubuntu/playbook/add_inventory.py

The command above should be launched on the configuration server with cron.



## Roles

There are three roles, described below.

### monarcco

Common tasks for the front and the back-office.

### monarcbo

[Backoffice](https://github.com/monarc-project/MonarcAppBO).
Only one per environment (dev, preprod, prod...).

### monarcfo

[Frontoffice](https://github.com/monarc-project/MonarcAppFO).
Can be multiple installation per environment to balance to the load.


## Python scripts

The `add_inventory.py` and `del_inventory.py` scripts are used to dynamically
edit the inventory files of the configuration server.
