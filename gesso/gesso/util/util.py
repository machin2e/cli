import os, sys
import psutil
import socket
import json, yaml
import time
import netifaces
import logging
import pkg_resources
from tinydb import TinyDB, Query

# -----------------------------------------------------------------------------
# Process Management
# -----------------------------------------------------------------------------

def kill_proc_tree(pid, including_parent=True):    
	parent = psutil.Process(pid)
	children = parent.children(recursive=True)
	for child in children:
		child.kill()
	gone, still_alive = psutil.wait_procs(children, timeout=5)
	if including_parent:
		parent.kill()
		parent.wait(5)

# -----------------------------------------------------------------------------
# Network Management
# -----------------------------------------------------------------------------

def get_inet_addresses():
	addresses = []
	for iface_name in netifaces.interfaces():
		#iface_addresses = [i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr': 'No IP addr'}])]
		#iface_addresses = [i['addr'] for i in netifaces.ifaddresses(iface_name).setdefault(netifaces.AF_INET, [{'addr': None}])]
		for i in netifaces.ifaddresses(iface_name).setdefault(netifaces.AF_INET, [{'addr': None}]):
			if not i['addr'] == None:
				addresses.append(i['addr'])
	return addresses

# -----------------------------------------------------------------------------
# File I/O
# -----------------------------------------------------------------------------

def load_yaml_file(path):
    # TODO: load .yaml file with model for particular (id, version) and populate this model... create __init__ to do that... multiple constructors!
    #component_model = 'model-component-gesso.yaml'
    yaml_object = None

    with open(path, 'r') as file:
        yaml_string = file.read()
        yaml_object = yaml.load(yaml_string)
        #print component_model
        return yaml_object

    return None

# -----------------------------------------------------------------------------
# File System Management
# -----------------------------------------------------------------------------

def get_file_list(path=os.getcwdu()):
	file_names = os.listdir(path)
	return file_names

# Checks if the current directory contains the specified file
# If so, returns the path containing the file. If not, returns None.
def contains_file(path=os.getcwdu(), filename=None):
	# TODO: rename to locate_file
	file_path = os.path.join(path, filename)
	if os.path.exists(file_path):
		return path
	else:
		return None

# Checks if the current directory or parent directory contains the specified file, recursively, starting with the specified path.
# If so, returns the path containing the file.
def parent_contains(filename, path=os.getcwdu(), recursive=True):
	# TODO: rename to locate_file
	file_path = os.path.join(path, filename)
	if os.path.exists(file_path):
		return path

	if recursive:
		parent_dir_path = os.path.abspath(os.path.join(path, os.pardir))
		is_root_dir = parent_dir_path == path
		if not is_root_dir:
			return parent_contains(filename, parent_dir_path)
		else:
			return parent_contains(filename, parent_dir_path, recursive=False)
	else:
		return None

def get_gesso_root(path=os.getcwdu()):
	return parent_contains('.gesso')

def is_gesso_root(path=os.getcwdu()):
	return path == get_gesso_root(path)

def is_gesso_tree(path=os.getcwdu()):
	if parent_contains('.gesso'):
		return True
	else:
		return False

def init_workspace_path(path=get_gesso_root()):

	# make "./.gesso/vagrant" folder if doesn't exist
	# make "./.gesso/vagrant/<vm-name>" folder for generated name
	# generate ./.gesso/vagrant/<vm-name>" Vagrantfile
	#    - modify to set the name of the VM
	#    - add bootstrap.sh
	#         - run "gesso init <vm-name>" on VM

	gesso_path = os.path.join(path, '.gesso')
	if not os.path.exists(gesso_path):
		print 'mkdir %s' % gesso_path 
		os.makedirs(gesso_path)
	
	components_path = os.path.join(path, '.gesso', 'components')
	if not os.path.exists(components_path):
		print 'mkdir %s' % components_path 
		os.makedirs(components_path)

def init_machine_path(name, path=get_gesso_root()):

	init_workspace_path(path)

	# Example filesystem:
	#
	# .gesso
	#     /components
	#         /fuzzy-koala
	#             /vagrant    
	#                 .Vagrantfile

	machine_path = os.path.join(path, '.gesso', 'components', name)
	if not os.path.exists(machine_path):
		print 'mkdir %s' % machine_path
		os.makedirs(machine_path)

	#if virtual:
	#vagrant_path = os.path.join(path, '.gesso', 'components', name, 'vagrant')
	#if not os.path.exists(vagrant_path):
	#	print 'mkdir %s' % vagrant_path
	#	os.makedirs(vagrant_path)
	
	return machine_path

def get_machine_path(name, path=get_gesso_root()):
	return os.path.join(path, '.gesso', 'components', name)

# TODO: Add to Device/Database class (serves as data access interface/map to component)
def get_machine_address(name):
	gesso_db_path = get_database_path()
	db = TinyDB(gesso_db_path, default_table='gesso')
	component_table = db.table('component')

	component = None

	Device = Query()
	component_element = component_table.search(Device.name == name)
	if len(component_element) > 0:
		component = component_element[0]
	
	return component['address']['ip4']

# Get machines from database
def get_machines():
	gesso_db_path = get_database_path()
	db = TinyDB(gesso_db_path, default_table='gesso')
	component_table = db.table('component')

	#component = None

	#Device = Query()
	#component_element = component_table.search(Device.name == name)
	#if len(component_element) > 0:
		#component = component_element[0]
	
	#return component['address']['ip4']
	return component_table.all()

def logger(log_name):
	"""
	Returns a logger for the log located at '.gesso/logs/<log_name>'.
	If the log doesn't exist, creates it in the '.gesso/logs' directory.
	"""

	#current_dir = os.getcwdu()
	gesso_root = get_gesso_root()
	#TODO: if gesso_root != None:

	gesso_folder = os.path.join(gesso_root, '.gesso')
	if not os.path.exists(gesso_folder):
		print 'mkdir %s' % gesso_folder
		os.makedirs(gesso_folder)

	log_folder = os.path.join(gesso_root, '.gesso', 'logs')
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
	data_dir = pkg_resources.resource_filename('gesso', 'data')
	if not os.path.exists(data_dir):
		return None
	return data_dir

def get_data_filename(filename):
	if filename is '' or filename is None:
		return pkg_resources.resource_filename('gesso', 'data')
	else:
		return pkg_resources.resource_filename('gesso', 'data/%s' % filename)

def setup_gesso_dir():
	return None	

def get_current_dir():
	return os.getcwdu()

def get_parent_dir():
	return os.path.abspath(os.path.join(get_current_dir(), os.pardir)) 

def get_gesso_dir():
	return os.path.join(get_current_dir(), '.gesso')

# Load copy of file 
def get_file(name):
	return open(get_data_filename(name)).read()

# Load copy of Vagrantfile
def get_vagrant_file(name):
	vagrantfiledata = get_data_filename('Vagrantfile')
	vagrantfiledata = open(vagrantfiledata).read().replace('%NAME%', name)
	return vagrantfiledata

# Load the Builderfile into a dictionary
def load_gessofile(path=get_gesso_root()):
	gesso_config_path = os.path.join(path, '.gesso', 'config')

	# Load the record from database
	gesso_config = {}
	with open(gesso_config_path, 'r') as file:
		gesso_config = json.loads(file.read())
		#gessofile_json = json.dumps(gessofile, indent=4, sort_keys=False)

	return gesso_config

# TODO: class Database:

# Get the path to SQLite database
def get_database_path(path=get_gesso_root()):
	gesso_db_path = os.path.join(path, '.gesso', 'database')
	return gesso_db_path

# Write updated database
def store_gessofile(gessofile, path=os.getcwdu()):
	gessofile_json = json.dumps(gessofile, indent=4, sort_keys=False)
	with open(path, 'w') as file:
		file.write(gessofile_json)
	#logger.info('---\n%s\n---' % db_dict_json)
