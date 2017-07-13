# Ansible playbook for MONARC deployement

This playbook is used to deploy MONARC installation.

## Requirements

* install Python 2 in all virtual machines;

## Usage

    $ git clone https://github.com/monarc-project/ansible-ubuntu.git
    $ cd ansible-ubuntu/
    $ ansible-playbook -i ../inventory/ monarc.yaml -u monarc -k -K



There are three roles, described below.


## monarcco

Common tasks for front and backoffice

## monarcbo

[Backoffice](https://github.com/CASES-LU/MonarcAppBO). Only one per environment (dev, preprod, prod...). 

## monarcfo

[Frontoffice](https://github.com/CASES-LU/MonarcAppFO). Can be multiple installation per environment to balance to the load.


## Python scripts

The `add_inventory.py` and `del_inventory.py` files are used to
dynamically edit the inventory files
