import subprocess
import os
import sys
import socket, json
import time
import util

def ssh(name=None):
	current_dir = os.getcwd()
	device_ip = util.request_ip_address(name)
	if device_ip != None:
		subprocess.call(['ssh', '-l', 'vagrant', device_ip])

if __name__ == "__main__":
	ssh()
