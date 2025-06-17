#!/bin/bash

# Executes the steps to deploy a new instances of MonarcAppFO, MonarAppBO

if [ ! $# -eq 2 ]
  then
    echo "2 arguments are required, and the 3rd one is optional. Usage:"
    echo "./deploy_new_release.sh PLAYBOOK_PATH ANSIBLE_PATH RELEASE_TAG"
    exit 1
fi

ANSIBLE_PATH=$1
PLAYBOOK_PATH=$2

TIME_START=$(date +%s)

AUTH="Authorization: token $GITHUB_AUTH_TOKEN"

echo $AUTH

# Retrieve a release tag to deploy fo, if not passed as an argument.
if [ -z "$3" ]
  then
    RELEASE_TAG=$(curl --silent -sH "$AUTH" -H 'Content-Type: application/json' https://api.github.com/repos/monarc-project/MonarcAppFO/releases/latest | jq  -r '.tag_name')
  else
    RELEASE_TAG=$1
fi

echo $RELEASE_TAG

FO_RELEASE_HASH=$(curl --silent -sH "$AUTH" -H 'Content-Type: application/json' -s https://api.github.com/repos/monarc-project/MonarcAppFO/commits/"$RELEASE_TAG"  | jq -r '.sha')

echo $FO_RELEASE_HASH

#./prepare_release_inventory.py

#cd $PLAYBOOK_PATH

echo "Running ansible..."
$ANSIBLE_PATH -i ../inventory/ deploy.yaml --user ansible --extra-vars "version=$RELEASE_TAG;release_hash=$FO_RELEASE_HASH"
