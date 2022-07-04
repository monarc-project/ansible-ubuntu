# Ansible playbook for MONARC deployement

This playbook is used to deploy the whole MONARC architecture in accordance to
the figure below.

![MONARC architecture](images/monarc-architecture.png "MONARC architecture")


### Ansible roles

There are three main roles, described below.

### monarcco

Common tasks for the front office and the back office.

### monarcbo

[Backoffice](https://github.com/monarc-project/MonarcAppBO).

### monarcfo

[Frontoffice](https://github.com/monarc-project/MonarcAppFO).
Can be multiple installation per client to balance to the load.

### extra roles

`role-apache2` and `role-certbot` are extra generic utility roles

## Requirements

* Python 3 on all servers;
* [Ansible](https://www.ansible.com/) must be installed on the configuration
  server;
* [PyMySQL](https://pypi.org/project/PyMySQL) on the BO and the FO; installed
  through role `monarcco`
* Postfix on the BO and all FO servers (for the password recovery feature of
  MONARC).


Python 3 should be the default on the system. For example:

```bash
$ python --version
Python 3.10.0
```
These roles have been tested with Ansible 2.9.6 - as shipped by default with
Ubuntu 20.04; you can use the packaged version or another more recent version
(from pip, poetry, virtualenv, ...)

Get the playbook for MONARC and install Ansible on the configuration server:

```bash
$ git clone https://github.com/monarc-project/ansible-ubuntu.git
$ cd ansible-ubuntu/
```

Poetry is not mandatory but convenient to manage the dependencies. Installation
is described [here](https://github.com/python-poetry/poetry#installation=).

```bash
$ poetry install
$ poetry shell
```

## Configuration

### SSH

* create a user named *ansible* on each server:
  * ``sudo adduser ansible``
* generate a SSH key for the user *ansible* on the configuration server:
  * ``ssh-keygen -t rsa -C "your_email@example.com"``
* from the configuration server:
  * ``ssh-copy-id ansible@BO``
  * ``ssh-copy-id ansible@FO``
  * ``ssh-copy-id ansible@RPX``

At that point you can check that it is possible to connect from the
configuration server to the other servers without having to enter a password.

### Unix groups

* add the user *ansible* in the *sudo* group:
  * ``sudo usermod -aG sudo ansible``
* give the permission to ansible to use sudo without password:
  * add ``ansible ALL=(ALL:ALL) NOPASSWD:ALL`` in the file */etc/sudoers* with *visudo*


### Ansible

* create a configuration file, _inventory/hosts_ with your own configuration:

```ini
[all:vars]
ansible_python_interpreter=/usr/bin/python3

# comment if you don't need a proxy
http_proxy="http://fqdn:3128/"
https_proxy="http://fqdn:3128/"
# docker config for statsservice
docker_config_bip="100.100.0.1/22"
docker_config_proxy="{{ http_proxy }}"

[monarc:vars]
env_prefix=""
publicHost="my.monarc.lu"
master="monarc-master.internal.monarc.lu"
monarc_statsservice_admin_token="<secret>"
monarc_statsservice_secret_key="<secret>"
monarc_statsservice_url="https://{{ publicHost }}/dashboard"

emailFrom="no-reply@{{ publicHost }}"
protocol="https"
bourlalias="monarcbo"

# front office systems
[dev]
monarc-fo1.internal.monarc.lu
monarc-fo2.internal.monarc.lu

# master / back office
[master]
monarc-master.internal.monarc.lu monarc_sql_password="<secret>"

# public facing reverse proxy
[rpx]
monarc-rpx.internal.monarc.lu

[monarc:children]
rpx
master
dev

```

A good test for connectivity and Ansible configuration would be to call
`ansible -m ping`; you should get an answer from all the FrontOffice servers,
the BackOffice and reverse proxy (rpx).

In the section ``[dev]``, ``monarc-fo1.internal.monarc.lu`` should be resolved
by the internal DNS. It is the internal name of the FrontOffice server. Same
for the other servers. If you can not change the internal DNS, it is possible
to handle this thanks to the file ``/etc/hosts`` of the system.

The variable `monarc_sql_password` is the password for the SQL database on the
BackOffice. Ansible will use it in order to create a new SQL user on the back
office with the corresponding databases.

Finally, launch Ansible from the `playbook` directory:

```bash
ansible@CFG:~/ansible-ubuntu/playbook$ ansible-playbook --diff monarc.yml
```

Ansible will install and configure the back office, the front office(s) and the
reverse proxy. Consequently the configuration server should be able to contact
these servers through SSH. For more details on how to execute Ansible read the
next section.




## Notes

### Updating the inventory of Ansible

Adding/removing a client to/from the Ansible inventory can be done with the
script `update.sh` via cron as the user `ansible`.

```bash
ansible@CFG:~$ crontal -l
0 *  * * *  /home/ansible/ansible-ubuntu/playbook/update.sh /home/ansible/ansible-ubuntu/playbook/ $BO_ADDRESS `which ansible-playbook` `which python3`
```

Optionally as a fourth argument you can specify the Python executable
(environment) to use.
This is an example. Below is a real world example:

```bash
ansible@monarc2-conf:~/ansible-ubuntu$ poetry env info

Virtualenv
Python:         3.9.12
Implementation: CPython
Path:           /home/ansible/.cache/pypoetry/virtualenvs/ansible-ubuntu-EcXl-2U4-py3.9
Valid:          True

System
Platform: linux
OS:       posix
Python:   /usr



ansible@monarc2-conf:~/ansible-ubuntu$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
#0 * * * * /home/ansible/ansible-ubuntu/playbook/update.sh /home/ansible/ansible-ubuntu/playbook/ 172.18.13.71 /home/ansible/.cache/pypoetry/virtualenvs/ansible-ubuntu-EcXl-2U4-py3.9/bin/ansible /home/ansible/.cache/pypoetry/virtualenvs/ansible-ubuntu-EcXl-2U4-py3.9/bin/python
```

Instead of an IP you can use a name of the BO if it resolves internally.  
As you can see we have used the full path to the ansible executable. This is
to be sure that the script will use the correct version of Ansible.

The frequency of the task defined by cron is up to you.



The script ``update.sh`` will:

* update the inventory of Ansible;
* launch Ansible for the creation/suppression of clients;
* synchronize the template of deliveries.

The `add_inventory.py` and `del_inventory.py` scripts are used to dynamically
edit the inventory files of the configuration server. These scripts are used by
``update.sh``.

You can use `list_inventory.py` to check all the current clients in the
inventory of Ansible. If you want to check the connectivity between the
configuration server and the front office servers:

```bash
ansible@CFG:~$ ./list_inventory.py ../inventory/ | cut -f 1 -d ' ' | uniq | xargs -n 1 ping -w 1
```

### Inventory migrations

If you have an old installation.

#### 1. Add statsToken

This migration adds a Stats Service token (`statsToken`) to the clients without this token.

```bash
ansible@CFG:~/ansible-ubuntu/inventory/migrations$ ./001-add_stats_token_to_inventory.py ../
```


### TLS certificate

#### Self-signed certificate

Generation of the certificate:

```bash
# openssl req -x509 -nodes -days 1000 -newkey rsa:2048 -keyout /etc/sslkeys/monarc.key -out /etc/sslkeys/monarc.crt
```

And then edit `playbook/monarc.yml` to set `SSLCertificateFile:` and
`SSLCertificateKeyFile:`, you **must** certbot support by setting
`certbot_enabled: false`

#### Let's Encrypt certificate

By default the playbook will attempt to generate a X509 ("https") certificate
using certbot and Let's Encrypt.

You don't need to set anything but you reverse proxy need an access to Let's
Encrypt API servers - if you set up `http_proxy` values in inventory the
certbot role will perform the right config for the renewal

The value of `emailFrom` will be used for the contact email while registering
the account with Let's Encrypt.

### Postfix

Installation of Postfix on the BO and the FO is **not done** by Ansible. You
have to do it manually.

## Issues

For security issues please contact us to
[info@cases.lu](mailto:info@cases.lu?subject=MONARC).

For other issues (ideas, improvements, etc.), you can directly submit
it to [GitHub](https://github.com/monarc-project/MonarcAppFO/issues)
