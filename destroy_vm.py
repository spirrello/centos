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


destroy_parser = argparse.ArgumentParser(
       description='Process args for destorying KVM guests.')
   

destroy_parser.add_argument('-de', '--destroy', required=False, action='store',
                   help='Destroy VMs.  Include the name of VM to destory.')
destroy_args = destroy_parser.parse_args()
if destroy_args:
    os.system("virsh start " + destroy_args)
    os.system("virsh destroy " + destroy_args)
    os.system("virsh undefine " + destroy_args)
    print("Deleting the VM image....")
    os.system("rm -f /var/lib/libvirt/images/" + destroy_args + ".img")
    sys.exit()