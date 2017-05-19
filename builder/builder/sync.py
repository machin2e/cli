import subprocess
import os
import sys

import pexpect

def sync2(name):
	#cwd = os.path.dirname(os.path.realpath(__file__))
	#cwd = os.path.join(os.getcwd(), '.builder', 'vagrant')
	#cwd = os.path.join(os.path.dirname(__file__), '.builder', 'vagrant')
	#print cwd 

	device_name = 'great-spider'
	device_ip = '192.168.1.9'
	p = pexpect.spawn('unison %s ssh://%s//builder' % (device_name, device_ip), cwd=os.getcwd())
	p.setecho(False)

def sync(name):
	#process = subprocess.Popen(['vagrant', 'ssh', name], stdout=subprocess.PIPE, cwd=os.path.dirname(os.path.realpath(__file__)), bufsize=1)
	cwd = os.path.dirname(os.path.realpath(__file__))
	print cwd 
	username = 'vagrant'
	device_name = name #device_name = 'great-spider' # TODO: Send message to great-spider to get its IP.
	device_ip = '192.168.1.27'    # TODO: Use IP to log into the device.
	process = subprocess.Popen(['unison', '-auto', '-batch', device_name, 'ssh://vagrant@%s//builder' % device_ip ], 
	                           stdout=subprocess.PIPE,
							   stdin=subprocess.PIPE,
							   shell=False,
							   cwd=os.getcwd(),
							   bufsize=1)

	while True:
		#output = process.stdout.readline()
		output = process.stdout.read(1)
		if output == '' and process.poll() is not None:
			break
		if output:
			sys.stdout.write(output)
			sys.stdout.flush()
			#print output.strip(),

if __name__ == "__main__":
	ssh()
