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


Install ansible on the configuration server and get the playbook for MONARC:

    $ sudo apt-get install ansible
    $ git clone https://github.com/monarc-project/ansible-ubuntu.git
    $ cd ansible-ubuntu/

### Configuration

* create a user named *ansible* on each server;
* add the IP of the BO, FO and RPX in the file */etc/hosts* of the
  configuration server;
* from the configuration server: ``ssh-copy-id ansible@BO/FO/RPX``
* add the user *ansible* in the *sudo* group:
  * ``sudo usermod -aG sudo ansible``
* add the user *www-data* in the *ansible* group:
  * ``sudo usermod -aG  ansible www-data``
* give the permission to ansible to use sudo without password:
  * add ``ansible  ALL=(ALL:ALL) NOPASSWD:ALL`` in the file */etc/sudoers*
* create a file _inventory/hosts_:

        [dev]
        FQDN-FO

        [dev:vars]
        master= "FQDN-BO"
        publicHost= "FQDN-RPX"
        clientDomain= ""


        [master]
        FQDN-BO monarc_sql_password="<password>"


        [rpx]
        FQDN-RPX


        [monarc:children]
        rpx
        master
        dev


        [monarc:vars]
        env_prefix=""
        clientDomain= ""
        github_auth_token="<your-github-auth-token>"

  The variable *monarc\_sql\_password* is the password for the SQL database
  on the BO.


* finally, launch ansible:

        $ cd playbook/
        $ ansible-playbook -i ../inventory/ monarc.yaml --user ansible


### Notes

1. Adding an attribute for the ansible inventory is done with the command:

        $ ssh ansible@BO sudo -u www-data /usr/local/bin/new_monarc_clients.sh | ./add_inventory.py ../inventory/
        $ ansible-playbook -i ../inventory/ monarc.yaml --user ansible

The command above should be launched on the configuration server with ``cron``.


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
