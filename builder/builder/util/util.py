import os, sys
import psutil
import socket, json
import time
import netifaces
import logging
import pkg_resources

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

def get_inet_addresses():
	addresses = []
	for iface_name in netifaces.interfaces():
		#iface_addresses = [i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr': 'No IP addr'}])]
		#iface_addresses = [i['addr'] for i in netifaces.ifaddresses(iface_name).setdefault(netifaces.AF_INET, [{'addr': None}])]
		for i in netifaces.ifaddresses(iface_name).setdefault(netifaces.AF_INET, [{'addr': None}]):
			if not i['addr'] == None:
				addresses.append(i['addr'])
	return addresses

# Initialize logging folder.
# Setup log folder in `.builder/logs/`.
def setup_log_folder(log_name):

	current_dir = os.getcwdu()

	builder_folder = os.path.join(current_dir, '.builder')
	if not os.path.exists(builder_folder):
		print 'mkdir %s' % builder_folder
		os.makedirs(builder_folder)

	log_folder = os.path.join(current_dir, '.builder', 'logs')
	if not os.path.exists(log_folder):
		print 'mkdir %s' % log_folder 
		os.makedirs(log_folder)

	logfile_name = '%s.log' % log_name
	logfile_path = os.path.join(log_folder, logfile_name)
	#logging.basicConfig(filename=logfile_path, level=logging.DEBUG, format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
	logger = logging.getLogger(log_name)
	logger.setLevel(logging.DEBUG)
	# Create file handler that stores the logged messages
	fh = logging.FileHandler(logfile_path)
	fh.setLevel(logging.DEBUG)
	# Create formatter and add it to handlers
	formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	#return logfile_path
	return logger

def get_data_dir():
	data_dir = pkg_resources.resource_filename('builder', 'data/')
	if not os.path.exists(data_dir):
		return None
	return data_dir

def get_data_filename(filename):
	return pkg_resources.resource_filename('builder', 'data/%s' % filename)

def setup_builder_dir():
	return None	

def get_current_dir():
	return os.getcwdu()

def get_parent_dir():
	return os.path.abspath(os.path.join(get_current_dir(), os.pardir)) 

def get_builder_dir():
	return os.path.join(get_current_dir(), '.builder')

# Load copy of file 
def get_file(name):
	return open(get_data_filename(name)).read().replace('%NAME%', name)

# Load copy of Vagrantfile
def get_vagrant_file(name):
	vagrantfiledata = get_data_filename('Vagrantfile')
	vagrantfiledata = open(vagrantfiledata).read().replace('%NAME%', name)
	return vagrantfiledata

#
# Networking
#

def request_ip_address(name=None):
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

			# Deserialize JSON
			response = json.loads(data)

			# Check for matching device name. If it matches, return the IP address.
			if (response['name'] == name):
				#print "%s\t%s" % (data, fromaddr[0])
				s.close()
				return fromaddr[0]
		except:
			None
		current_time = int(round(time.time() * 1000))
	s.close()

	return None
