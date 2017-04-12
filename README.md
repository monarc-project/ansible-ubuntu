# Ansible playbook for MONARC deployement

This playbook is used to deploy monarc installation. There is three roles describe below.

## monarcco

Common tasks for front and backoffice

## monarcbo

[Backoffice](https://github.com/CASES-LU/MonarcAppBO). Only one per environment (dev, preprod, prod...). 

## monarcfo

[Frontoffice](https://github.com/CASES-LU/MonarcAppFO). Can be multiple installation per environment to balance to the load.


## Python scripts

The `add_inventory.py` and `del_inventory.py` files are used to
dynamically edit the inventory files
