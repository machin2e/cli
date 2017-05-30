# The Builderfile is used to bootstrap the Builder daemon which manages 
# the device's configuration and allows it to be edited in real-time 
# from smartphone and when plugged in over USB as mass storage.

# Create "Builderfile" that contains:
# - UUID
# - human-readable name

import os, sys
import subprocess
import uuid
import petname
import util
import json

def add(name, virtual=True):

	if name == None:
		name = petname.Generate(2)

	machine_path = init_machine_path(name)

	log_path = os.path.join(util.get_builder_root(), '.builder', 'logs')
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
		# TODO: save vagrant log in '.builder/logs/vagrant.log'

	# Generate copy of Vagrantfile from template file
	with open(os.path.join(machine_path, 'Vagrantfile'), 'w+') as file:
		vagrantfile_content = util.get_vagrant_file(name)
		file.write(vagrantfile_content)

	sys.stdout.write(' OK.\n')
	sys.stdout.flush()

	# Start virtual machine
	with open(vagrant_log_path, 'w+') as log:
		sys.stdout.write('Booting VM.')
		sys.stdout.flush()
		#process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE, cwd=machine_path)
		process = subprocess.Popen(['vagrant', 'up'], stdout=log, cwd=machine_path)
		process.wait()
		sys.stdout.write(' OK.\n')
		sys.stdout.flush()

	# TODO: CLI style where you enter high level commands with minimum info to start a interactive questionairre prompting for variable values (but with defaults assigned), also skippable, and if skipped, added to "todos".

	# TODO: Hello there.
	# How are you?
	# ...
	# // this will trigger refactoring moving "TODO" on top of "Hello there". (Make a little continuous-running vim robot (scripted inline right in Vim. Make it a plugin!)).
	#while True:
		#output = process.stdout.readline()
		#output = process.stdout.read(1)
		#if output == '' and process.poll() is not None:
			#break
		#if output:
			#sys.stdout.write(output)
			#sys.stdout.flush()
			#print output.strip(),

def init_workspace_path(path=util.get_builder_root()):

	# make "./.builder/vagrant" folder if doesn't exist
	# make "./.builder/vagrant/<vm-name>" folder for generated name
	# generate ./.builder/vagrant/<vm-name>" Vagrantfile
	#    - modify to set the name of the VM
	#    - add bootstrap.sh
	#         - run "builder init <vm-name>" on VM

	builder_path = os.path.join(path, '.builder')
	if not os.path.exists(builder_path):
		print 'mkdir %s' % builder_path
		os.makedirs(builder_path)
	
	devices_path = os.path.join(path, '.builder', 'devices')
	if not os.path.exists(devices_path):
		print 'mkdir %s' % devices_path 
		os.makedirs(devices_path)

def init_machine_path(name, path=util.get_builder_root()):

	init_workspace_path(path)

	# Example filesystem:
	#
	# .builder
	#     /devices
	#         /fuzzy-koala
	#             /vagrant    
	#                 .Vagrantfile

	machine_path = os.path.join(path, '.builder', 'devices', name)
	if not os.path.exists(machine_path):
		print 'mkdir %s' % machine_path
		os.makedirs(machine_path)

	#if virtual:
	#vagrant_path = os.path.join(path, '.builder', 'devices', name, 'vagrant')
	#if not os.path.exists(vagrant_path):
	#	print 'mkdir %s' % vagrant_path
	#	os.makedirs(vagrant_path)
	
	return machine_path

if __name__ == "__main__":
	init()
