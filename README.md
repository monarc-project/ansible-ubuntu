# Ansible playbook for MONARC deployement

This playbook is used to deploy the whole MONARC architecture in accordance to
the figure below.

![MONARC architecture](images/monarc-architecture.png "MONARC architecture")


## Requirements

* install Python 2 on all servers. Actually ansible 2.2 features only a tech
  preview of Python 3 support;
* [ansible](https://www.ansible.com/) must be installed on the configuration
  server. We have tested with version 2.2.1.0 of ansible.


## Usage

Install ansible and get the ansible configuration repository:

    $ sudo apt-get install ansible
    $ git clone https://github.com/monarc-project/ansible-ubuntu.git
    $ cd ansible-ubuntu/

Create a file _inventory/hosts_:

    [dev]
    IP-OF-THE-FO

    [dev:vars]
    master= "IP/DOMAIN of the BO"
    publicHost= "IP/DOMAIN of the RPX"


    [master]
    IP-OF-THE-FO


    [rpx]
    IP-OF-THE-RPX


    [monarc:children]
    rpx
    master
    dev


    [monarc:vars]
    env_prefix=""


Then launch ansible:

    $ cd ansible-ubuntu/playbook
    $ ansible-playbook -i ../inventory/ monarc.yaml --user ansible -k -K

*-k -K* forces the SSH authentication by simple password. In this case
*sshpass* must be installed on the configuration server.

However, it is strongly recommended to use a SSH key associated to a user
dedicated to ansible. The *ansible* user must be created on each servers.
In this case, run the following command:

    $ ansible-playbook -i ../inventory/ monarc.yaml --user ansible --ask-sudo-pass


### Tips

* create a user named *ansible* on each server;
* add the *ansible* user in the groups:
  * **sudo**: __sudo usermod -aG sudo ansible__
  * **www-data**: __sudo usermod -aG www-data ansible__
* from the configuration server: __ssh-copy-id ansible@IP-OF-BO/FO/RPX__
* add the IP of the BO, FO and RPX in the file __/etc/hosts__ of the
  configuration server;


### Notes

1. Adding an attribute for the ansible inventory is done with the command:

    $ ssh monarc@IP-OF-THE-BO sudo -u www-data /usr/local/bin/new_monarc_clients.sh | ./ansible-ubuntu/playbook/add_inventory.py

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
