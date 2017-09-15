#!/bin/sh

# Run this script from the configuration server:
#
# ./prepare-server.sh IPrpx IPbo IPfo1 <host_username> <ansible_username> <ansible_email> <proxy_URL>

IP_RPX=$1
IP_BO=$2
IP_FO1=$3
HOST_USER_NAME=${4:-cases}
ANSIBLE_USER_NAME=${5:-ansible}
ANSIBLE_USER_PASSWORD="$(openssl rand -hex 32)"
ANSIBLE_USER_EMAIL=${6:-'info@cases.lu'}
PROXY=${7:-''}

sudo apt-get install -y python python-pip git
sudo -H pip install ansible dnspython

# Create a user for ansible
sudo useradd --create-home -s /bin/bash $ANSIBLE_USER_NAME
echo "$ANSIBLE_USER_NAME:$ANSIBLE_USER_PASSWORD" | sudo chpasswd
echo $ANSIBLE_USER_PASSWORD

# Generate a SSH key for the new user
sudo -u $ANSIBLE_USER_NAME ssh-keygen -t rsa -C "$ANSIBLE_USER_EMAIL"

if [ "$PROXY" != '' ]; then
    # set the proxy locally (i.e. on the configuration server)
    echo "export http_proxy=http://$PROXY" >> /home/$ANSIBLE_USER_NAME/.bashrc
    echo "export https_proxy=https://$PROXY" >> /home/$ANSIBLE_USER_NAME/.bashrc
fi


for ip in IP_RPX IP_BO IP_FO1; do
    echo "Configuring $ip..."
    ssh $HOST_USER_NAME@$ip -t " sudo useradd --create-home -s /bin/bash $ANSIBLE_USER_NAME ; sudo passwd $ANSIBLE_USER_NAME $ANSIBLE_USER_PASSWORD"

    sudo -u $ANSIBLE_USER_NAME ssh-copy-id $ip

    ssh $HOST_USER_NAME@$ip -t " sudo usermod -aG sudo $ANSIBLE_USER_NAME; usermod -aG  $ANSIBLE_USER_NAME www-data  ;  echo '$ANSIBLE_USER_NAME ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers"

    ssh $ANSIBLE_USER_NAME@$ip -t " sudo apt-get install -y python python-pip git"

    if [ "$PROXY" != '' ]; then
        # set the proxy
        ssh $ANSIBLE_USER_NAME@$ip -t " echo 'export http_proxy=http://$PROXY' >> /home/$ANSIBLE_USER_NAME/.bashrc  ;  echo 'export https_proxy=https://$PROXY' >> /home/$ANSIBLE_USER_NAME/.bashrc"
    fi
done

# return to HOST_USER_NAME user
exit

exit 0
