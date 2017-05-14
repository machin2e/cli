import os
import json
import subprocess
import psutil
import tempfile
import portalocker
from socket import *

def start():
	print "Starting service."
	current_file_path = os.getcwdu()
	p = subprocess.Popen(['builder', 'run', 'manager'], cwd=current_file_path)
	#p = subprocess.Popen(['builder', 'start', 'broadcast'], cwd=current_file_path)
	print p.pid

def stop():
	# Locate pidfile (if it exists)
	current_dir = os.getcwd()
	pidfile_path = os.path.join(tempfile.gettempdir(), 'builder.pid')

	# Read pid from pidfile
	pidfile = open(pidfile_path, "r")
	content = pidfile.readlines()
	pidfile.close()
	content = [x.strip() for x in content] # remove whitespace characters like `\n` at the end of each line
	# print content
	pid = int(content[0])

	# Kill process
	kill_proc_tree(pid)

	# Delete pidfile
	os.remove(pidfile_path)

def run():
	PORT = 4445

	# Write pid into pidfile
	current_dir = os.getcwd()
	#pidfile = os.path.join(current_dir, 'builder.pid')
	#pidfile = tempfile.NamedTemporaryFile()
	pidfile_path = os.path.join(tempfile.gettempdir(), 'builder.pid') # create the pidfile
	pidfile = open(pidfile_path, "w+")
	#portalocker.lock(pidfile, portalocker.LOCK_EX) # lock the pidfile
	pidfile.write('%s' % os.getpid())
	pidfile.close()

	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('', PORT))

	response_timeout = 2.0 # seconds

	#serverSocket.settimeout(response_timeout)
	serverSocket.setblocking(0)

	configuration = {}

	while True:
		try:
			message, address = serverSocket.recvfrom(1024)
			# print message, address

			if message.startswith("announce"):
				print "Received:", message, "from", address

			elif message.startswith("configure"):
				# e.g., "configuration key:value"
				data = message[len("configure") + 1:] # remove "echo " from start of string
				pair = data.split(':')
				key = pair[0]
				value = pair[1]
				configuration[key] = value
				response_message = "key: %s, value: %s" % (key, configuration[key])
				serverSocket.sendto(response_message, address)

				# Update configuration file on disk
				# TODO: Just update the in-memory and sync to disc periodically
				builderfile_path = 'fooBuilderfile'

				# Create default Builderfile if it doesn't exist.
				#if not os.path.exists(builderfile_path):
				file = open(builderfile_path, 'w')

				# Write entry in dictionary
				for key in configuration:
					file.write("%s:%s\n" % (key, configuration[key]))

				file.close()

			elif message.startswith("echo"):
				response_message = message[len("echo") + 1:] # remove "echo " from start of string
				print response_message
				serverSocket.sendto(response_message, address)

			elif message.startswith('list'):
				response_message = list2() # remove "echo " from start of string
				print response_message
				serverSocket.sendto(response_message, address)

		except:
			None

	serverSocket.close()

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)


def list2():
	builder_dir = os.path.abspath('/builder') # this will return current directory in which python file resides.
	builderfile_path = os.path.abspath(os.path.join(builder_dir, 'Builderfile')) # this will return current directory in which python file resides.
	# Read the Builderfile
	# TODO: Initialize the daemon here?
	file = open(builderfile_path, 'r')
	filelines = file.readlines()
	file.close()
	
	device_uuid = 'N/A'
	device_name = 'N/A'
	device_ip = 'N/A'

	for i in range(len(filelines)):

		# Read human-readable name 
		if filelines[i].startswith('name:'):
			device_name = filelines[i].split(': ')[1]
			device_name = device_name.replace('\n', '')

		# Read UUID
		if filelines[i].startswith('uuid:'):
			device_uuid = filelines[i].split(': ')[1]
			device_uuid = device_uuid.replace('\n', '')
	
	# Set IP address
	#device_ip = socket.gethostbyname(socket.gethostname())

	# Print the device listing
	#return "%s\t%s\t%s" % (device_name, device_uuid, device_ip)
	list_dict = {
		'name': device_name,
		'uuid': device_uuid
	}

	return json.dumps(list_dict)


if __name__ == "__main__":
	run()
