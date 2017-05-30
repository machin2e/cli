import subprocess
import os
import sys
import socket, json
import time
import util

def ssh(name=None):
	machine_path = util.get_machine_path(name)
	device_ip = util.request_ip_address(name) # TODO: lookup the IP address of the device (and if it's a VM, make sure it's running!)
	if device_ip != None:
		username = 'vagrant'
		subprocess.call(['ssh', '-l', username, device_ip], cwd=machine_path)

if __name__ == "__main__":
	ssh()
