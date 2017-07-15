# Ansible playbook for MONARC deployement

This playbook is used to deploy MONARC installation.


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
edit the inventory files.
