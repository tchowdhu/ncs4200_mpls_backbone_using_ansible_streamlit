#!/bin/sh

# -u $NCSUSER -k
if [ -z  "$2" ]; then
    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u $NCSUSER -i inventory $1 -e "ansible_python_interpreter=$PYTHONENV ansible_ssh_pass=$NCSPASS"
else
    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u $NCSUSER -i inventory $1 -e "ansible_python_interpreter=$PYTHONENV ansible_ssh_pass=$NCSPASS" $2
fi
