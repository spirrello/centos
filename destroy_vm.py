#!/usr/bin/python
"""
This script serves as a wrapper for installing KVM guests.

"""

import sys
import os
import time
import argparse
import crypt


parser = argparse.ArgumentParser(
       description='Process args for destorying KVM guests.')
   

parser.add_argument('-v', '--vm', required=False, action='store',
                   help='Destroy VMs.  Include the name of VM to destory.')
destroy_args = parser.parse_args()
if destroy_args:
    os.system("virsh start " + destroy_args.vm)
    os.system("virsh destroy " + destroy_args.vm)
    os.system("virsh undefine " + destroy_args.vm)
    print("Deleting the VM image....")
    os.system("rm -f /var/lib/libvirt/images/" + destroy_args.vm + ".img")
    sys.exit()