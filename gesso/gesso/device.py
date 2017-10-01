import os, sys, shutil
import subprocess
import json
import uuid
import petname
from tabulate import tabulate
from tinydb import TinyDB, Query

import util

def add(name, virtual=True):
	# TODO: Check if the machine already exists. Only add if the specified name doesn't already exist. If using a generated name, choose a unique name.

	if name == None:
		name = petname.Generate(2)

	machine_path = util.init_machine_path(name)

	log_path = os.path.join(util.get_gesso_root(), '.gesso', 'logs')
	vagrant_log_path = os.path.join(log_path, 'vagrant.log')

	# i.e., `vagrant init`
	sys.stdout.write('Initializing \'%s\'.' % name)
	sys.stdout.flush()
	#with open(os.devnull, 'w') as devnull:
	with open(vagrant_log_path, 'w+') as log:
		#process = subprocess.Popen(['vagrant', 'init', '-m', vagrant_box], stdout=subprocess.PIPE, cwd=machine_path, bufsize=1)
		#process = subprocess.Popen(['vagrant', 'init', '-m', vagrant_box], stdout=subprocess.PIPE, cwd=machine_path)
		process = subprocess.Popen(['vagrant', 'init'], stdout=log, cwd=machine_path)
		process.wait()
		# TODO: save vagrant log in '.gesso/logs/vagrant.log'

	# Generate copy of Vagrantfile from template file
	with open(os.path.join(machine_path, 'Vagrantfile'), 'w+') as file:
		vagrantfile_content = util.get_vagrant_file(name)
		file.write(vagrantfile_content)

	sys.stdout.write(' OK.\n')
	sys.stdout.flush()

	# Start VM
	start(name)

	# TODO: CLI style where you enter high level commands with minimum info to start a interactive questionairre prompting for variable values (but with defaults assigned), also skippable, and if skipped, added to "todos".

def list(name=None):

	machines = util.get_machines()

	# Generate table! Use tabulate if you can...
	columns = [ 'status', 'hostname', 'uuid', 'ip4', 'ip6' ]
	table_column_separator_width = 4 # spaces
	table_column_width = []
	table_rows = []

	#print 'name\tuuid\taddress (ip4)'
	for machine in machines:
		#print '%s%s%s%s%s' % (machine['name'], ' ' * 4, machine['uuid'], ' ' * 4, machine['address']['ip4'])
		table_row = []
		table_row.append(machine.get('status', 'N/A')) # returns machine['status'] or 'N/A' if 'name' key doesn't exist
		table_row.append(machine.get('name', 'N/A')) # returns machine['name'] or 'N/A' if 'name' key doesn't exist
		table_row.append(machine.get('uuid', 'N/A')) # returns machine['uuid'] or 'N/A' if 'name' key doesn't exist
		table_row.append(machine['address'].get('ip4', 'N/A')) # returns machine['address']['ip4'] or 'N/A' if 'name' key doesn't exist
		table_row.append(machine['address'].get('ip6', 'N/A')) # returns machine['address']['ip6'] or 'N/A' if 'name' key doesn't exist
		table_rows.append(table_row)
	
	print tabulate(table_rows, headers=columns)

# gesso device start golden-hornet
def start(name, background=True):
	# TODO: Determine if machine is a VM by checking if a Vagrantfile exists in the machine_path

	log_path = os.path.join(util.get_gesso_root(), '.gesso', 'logs')
	vagrant_log_path = os.path.join(log_path, 'vagrant.log')

	# Start virtual machine
	machine_path = util.get_machine_path(name)
	with open(vagrant_log_path, 'w+') as log:
		if background == True:
			sys.stdout.write('Starting VM in background. VM will be available in a few minutes. Check status with `gesso device list`.')
			sys.stdout.flush()
		elif background == False:
			sys.stdout.write('Starting VM.')
			sys.stdout.flush()

		#process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE, cwd=machine_path)
		process = subprocess.Popen(['vagrant', 'up'], stdout=log, cwd=machine_path)

		if background == False:
			process.wait()
			sys.stdout.write(' OK.\n')
			sys.stdout.flush()
			# TODO: Announce with voice "device <device-name> is now available."
			None

def ssh(name=None):
	machine_path = util.get_machine_path(name)
	address_ip4 = util.get_machine_address(name)
	#device_ip = util.request_ip_address(name) # TODO: lookup the IP address of the device (and if it's a VM, make sure it's running!)
	if address_ip4 != None:
		username = 'vagrant'
		subprocess.call(['ssh', '-l', username, '-o', 'StrictHostKeyChecking=no', address_ip4], cwd=machine_path)

def restart(name):
	# TODO: Determine if machine is a VM by checking if a Vagrantfile exists in the machine_path

	log_path = os.path.join(util.get_gesso_root(), '.gesso', 'logs')
	vagrant_log_path = os.path.join(log_path, 'vagrant.log')

	# Start virtual machine
	machine_path = util.get_machine_path(name)
	with open(vagrant_log_path, 'w+') as log:
		sys.stdout.write('Restarting VM.')
		sys.stdout.flush()
		#process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE, cwd=machine_path)
		process = subprocess.Popen(['vagrant', 'reload'], stdout=log, cwd=machine_path)
		process.wait()
		sys.stdout.write(' OK.\n')
		sys.stdout.flush()

def pause(name):
	# TODO: Determine if machine is a VM by checking if a Vagrantfile exists in the machine_path

	log_path = os.path.join(util.get_gesso_root(), '.gesso', 'logs')
	vagrant_log_path = os.path.join(log_path, 'vagrant.log')

	# Start virtual machine
	machine_path = util.get_machine_path(name)
	with open(vagrant_log_path, 'w+') as log:
		sys.stdout.write('Pausing VM.')
		sys.stdout.flush()
		#process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE, cwd=machine_path)
		process = subprocess.Popen(['vagrant', 'suspend'], stdout=log, cwd=machine_path)
		process.wait()
		sys.stdout.write(' OK.\n')
		sys.stdout.flush()

def stop(name):
	# TODO: Determine if machine is a VM by checking if a Vagrantfile exists in the machine_path

	log_path = os.path.join(util.get_gesso_root(), '.gesso', 'logs')
	vagrant_log_path = os.path.join(log_path, 'vagrant.log')

	# Start virtual machine
	machine_path = util.get_machine_path(name)
	with open(vagrant_log_path, 'w+') as log:
		sys.stdout.write('Stopping VM.')
		sys.stdout.flush()
		process = subprocess.Popen(['vagrant', 'halt'], stdout=log, cwd=machine_path)
		process.wait()
		sys.stdout.write(' OK.\n')
		sys.stdout.flush()

def remove(name):
	# TODO: Determine if machine is a VM by checking if a Vagrantfile exists in the machine_path
	# TODO: Check if machine is running. If so, shutdown before continuing. Verify that it's shut down.

	log_path = os.path.join(util.get_gesso_root(), '.gesso', 'logs')
	vagrant_log_path = os.path.join(log_path, 'vagrant.log') 
	# Destroy virtual machine
	machine_path = util.get_machine_path(name)
	if os.path.exists(machine_path):
		with open(vagrant_log_path, 'w+') as log:
			sys.stdout.write('Removing VM.')
			sys.stdout.flush()
			process = subprocess.Popen(['vagrant', 'destroy', '-f'], stdout=log, cwd=machine_path)
			process.wait()
			sys.stdout.write(' OK.\n')
			sys.stdout.flush()
		
	# Recursively delete the machine path
	# TODO: Check if machine is shutdown. It shouldn't be running when deleting the folder hierarchy.
	if os.path.exists(machine_path):
		sys.stdout.write('Deleting %s.' % machine_path)
		sys.stdout.flush()
		shutil.rmtree(machine_path)
		sys.stdout.write(' OK.\n')
		sys.stdout.flush()

	# Remove device from registry (in SQLite database) if it exists
	db_path = util.get_database_path()
	db = TinyDB(db_path, default_table='gesso')
	Device = Query()
	device = db.table('device').get(Device.name == name)
	if device != None:
		sys.stdout.write('Removing %s from database.' % name)
		sys.stdout.flush()

		Device = Query()
		#device = db.table('device').get(Device.name == name)
		removed_device_ids = db.table('device').remove(Device.name == name)
		if len(removed_device_ids) > 0:
			sys.stdout.write(' OK.')
			sys.stdout.flush()
		else:
			sys.stdout.write(' Error.')
			sys.stdout.flush()

	else:
		# The device was not in the database
		None

if __name__ == "__main__":
	init()
