The purpose of this repo is to have rev control on scripts used for deploying Centos on KVM.  This project uses Ansible and Python to automate the deployment
process.

Process
1.) Run kvm_wrapper.py directly on the KVM host to build the VMs.  Ex:
python kvm_wrapper.py -v vm7-1 -d local.net -s 192.168.122.101 -m 255.255.255.0 -g 192.168.122.1 -n 4.2.2.2 -u spirrell -e home

The script contains a help menu for assistance.


2.) Run install_sshkeys.yml without -K and with -k.
3.) Run install_prereqs.yml with -K
4.) Go to Contiv installation.

Requirements
- Ansible
- Working KVM installation
- DHCP server configured on KVM host
- 3 networks configured behind the KVM host