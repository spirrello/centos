#!/usr/bin/python
"""
This script serves as a wrapper for installing KVM guests.

"""

import sys
import os
import time
import getpass
import argparse
import crypt


def install_prereqs(environment):
    """This method will run the install_prereqs playbook to install the standard packages."""
    os.system("ansible-playbook playbooks/install_prereqs.yaml --inventory-file=playbooks/environments/" + environment.strip() + "/inventory -K")


def build_kickstart(args,password_var):
    """This method will build the kickstart file."""
    
    if args.static_ip == "":
        os.system("ansible-playbook playbooks/generate_kickstart.yml --extra-vars \"username=" + args.username + " user_password=" + password_var + " vm_name=" + args.vm + " domain=" + args.domain + "\" --inventory-file=playbooks/environments/" + args.env + "/inventory")
    else:
        try:
            os.system("ansible-playbook playbooks/generate_kickstart.yml --extra-vars \"username=" + args.username + \
                " user_password=" + password_var + " vm_name=" + args.vm + " domain=" + \
                args.domain + " static_ip=" + args.static_ip + " mask=" + args.mask + " gateway=" + \
                args.gateway + " dns=" + args.dns + "\" --inventory-file=playbooks/environments/" + args.env + "/inventory")
        except Exception as e:
            print("Error with the arguments...something is missing.  Error:")
            print (str(e))

       
def build_vm(kickstart_file, args):
    os.system("virt-install --connect qemu:///system -n " + args.vm + " -r 1024 --vcpus=1 \
      --disk path=/var/lib/libvirt/images/"+ args.vm +".img,size=10 --graphics \
      vnc,listen=0.0.0.0 --noautoconsole --os-type linux --os-variant rhel7 \
      --accelerate --network=bridge:virbr0 --initrd-inject=" + args.vm + ".cfg \
      --extra-args="'ks=file:'"" + args.vm + ".cfg --hvm --location /var/lib/libvirt/boot/CentOS-7-x86_64-Minimal-1511.iso")


def get_password():
    """Encrypt the user password"""
    password_var = crypt.crypt(getpass.getpass(prompt="Please enter user password:"),"232e*&7$asdfasdfasdf")
    return password_var


def main():
   parser = argparse.ArgumentParser(
       description='Process args for building KVM guests.')
   parser.add_argument('-v', '--vm', required=True, action='store',
                       help='VM name')
   parser.add_argument('-d', '--domain', required=True, action='store',
                       help='VM domain')
   parser.add_argument('-s', '--static_ip', required=False, action='store',
                       help='static IP')
   parser.add_argument('-m', '--mask', required=False, action='store',
                       help='Net Mask')
   parser.add_argument('-g', '--gateway', required=False, action='store',
                       help='Gateway')
   parser.add_argument('-n', '--dns', required=False, action='store',
                       help='Name Server')
   parser.add_argument('-u', '--username', required=True, action='store',
                       help='User name to include in the VM build.')
   parser.add_argument('-e', '--env', required=True, action='store',
                       help='Environment...home,office,etc.')
   
   args = parser.parse_args()
   password_var = get_password()
   

   #Build the kickstart file.
   build_kickstart(args,password_var)

   #Build VM
   kickstart_file = args.vm + ".cfg"
   build_vm(kickstart_file, args)


# Start program
if __name__ == "__main__":
   main()
