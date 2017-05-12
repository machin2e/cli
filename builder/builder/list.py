import os, sys, time
import socket
import uuid

def list():
	PORT = 4445

	#device_uuid = uuid.uuid4()
	#print "uuid: %s" % uuid

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
			print "Response from %s:%s: %s" % (fromaddr[0], fromaddr[1], data)
		except:
			None
		current_time = int(round(time.time() * 1000))
	s.close()

def list2():
	builderfile_path = './Builderfile'




	# Read the Builderfile
	# TODO: Initialize the daemon here?
	file = open(builderfile_path, 'r')
	filelines = file.readlines()
	
	device_uuid = 'N/A'
	device_name = 'N/A'
	device_ip = 'N/A'

	for i in range(len(filelines)):

		# Read UUID
		if filelines[i].startswith('UUID:'):
			device_uuid = filelines[i].split(': ')[1]
			device_uuid = device_uuid.replace('\n', '')

		# Read human-readable name 
		if filelines[i].startswith('Name:'):
			device_name = filelines[i].split(': ')[1]
			device_name = device_name.replace('\n', '')

	# Print the device listing
	print "%s\t%s\t%s" % (device_name, device_uuid, device_ip)

	file.close()

	# List VMs (if any)
	current_dir = os.getcwdu()
	builder_dir = os.path.abspath(os.path.join(current_dir, '.builder'))
	vagrant_dir = os.path.abspath(os.path.join(builder_dir, 'vagrant'))

	virtual_machines = []
	for dir in os.listdir(vagrant_dir):
		machine_dir = os.path.abspath(os.path.join(vagrant_dir, dir))
		if os.path.isdir(machine_dir):
			Vagrantfile_path = os.path.abspath(os.path.join(machine_dir, 'Vagrantfile'))
			if os.path.exists(Vagrantfile_path):
				virtual_machines.append(dir)

	for machine_name in virtual_machines:
		device_uuid = 'N/A'
		device_name = machine_name
		device_ip = 'N/A'
		# Print the device listing
		print "%s\t%s\t%s" % (device_name, device_uuid, device_ip)


if __name__ == "__main__":
	list()
