import os, sys
import pexpect, subprocess
import time
import socket, json

def sync2(name):
	#cwd = os.path.dirname(os.path.realpath(__file__))
	#cwd = os.path.join(os.getcwd(), '.builder', 'vagrant')
	#cwd = os.path.join(os.path.dirname(__file__), '.builder', 'vagrant')
	#print cwd 

	device_name = 'great-spider'
	device_ip = '192.168.1.9'
	p = pexpect.spawn('unison %s ssh://%s//builder' % (device_name, device_ip), cwd=os.getcwd())
	p.setecho(False)

def list(name=None):
	PORT = 4445

	broadcast_address = '192.168.1.255' # '<broadcast>'
	response_timeout = 2.0 # seconds

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	# s.settimeout(response_timeout)
	s.setblocking(0)

	data = "list"
	s.sendto(data, (broadcast_address, PORT)) # Works

	response_start_time = int(round(time.time() * 1000))
	current_time = 0
	timeout = 2500

	while current_time - response_start_time < timeout:
		try:
			data, fromaddr = s.recvfrom(1000)
			
			response = json.loads(data)
			sys.stdout.write("%s\t%s" % (response, fromaddr[0]))
			sys.stdout.flush()
			if (response['name'] == name):
				#print "%s\t%s" % (data, fromaddr[0])
				s.close()
				return fromaddr[0]

			# TODO: create directories in builder_dir for the discovered VM if it doesn't already exist
			#create_builer_folder(builder_name)
			#create_builder_folder(data)
		except:
			None
		current_time = int(round(time.time() * 1000))
	s.close()

	return None

def sync(name, username='vagrant'):
	#process = subprocess.Popen(['vagrant', 'ssh', name], stdout=subprocess.PIPE, cwd=os.path.dirname(os.path.realpath(__file__)), bufsize=1)
	cwd = os.path.dirname(os.path.realpath(__file__))
	device_name = name #device_name = 'great-spider' # TODO: Send message to great-spider to get its IP.
	device_ip = '192.168.1.31'    # TODO: Use IP to log into the device.

	# TODO: Cache this!
	device_ip = list(name)
	print "DEVICE:", device_ip

	#process = subprocess.Popen(['unison', '-sshargs "-o StrictHostKeyChecking=no"', '-auto', '-batch', device_name, 'ssh://vagrant@%s//builder' % device_ip ], 
	process = subprocess.Popen(['unison', '-sshargs', "'-o StrictHostKeyChecking=no'", '-auto', '-batch', device_name, 'ssh://vagrant@%s//builder' % device_ip ], 
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
