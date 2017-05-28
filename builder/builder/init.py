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

def init(name=None, virtual=False):
	if virtual == True:
		init_virtual(name, virtual)
	else:
		init_physical(name, virtual)

def init_physical(name=None, virtual=False):

	# Check if cwd contains .builder, or if any of it's parents contain one (if so, we're in a builder repository)
	#	If not, create it and populate it with a 'config' file that will contain initial config
	#	If so, print error 'Current/parent directory already contains a .builder folder'

	parent_path = util.parent_contains('.builder')
	if not parent_path is None:
		print 'Error: I can\'t do that.'
		print 'Reason: There is already a .builder directory at %s.' % parent_path
		print 'Hint: Use `cd` to change to a different directory.' 

	else:

		# Initialize the builder root file system
		current_path = os.getcwdu()
		builder_dir_path = os.path.join(current_path, '.builder')
		builder_config_path = os.path.join(builder_dir_path, 'config')

		builder_path = os.path.join(current_path, '.builder')
		if not os.path.exists(builder_path):
			print 'mkdir %s' % builder_path 
			os.makedirs(builder_path)

		# Initialize builder config file
		builder_config = {
			'name': petname.Generate(2) if name == None else name,
			'uuid': str(uuid.uuid4()), # TODO: read UUID from hardware!
			'project': 'none',
			'role': 'none',
			'project': 'none'
		}
		builder_config_json = json.dumps(builder_config, indent=4, sort_keys=False)

		builder_config_path = os.path.join(current_path, '.builder', 'config')
		if not os.path.exists(builder_config_path):
			print 'touch %s' % builder_config_path 
			with open(builder_config_path, 'w+') as file:
				file.write(builder_config_json)

		# TODO: Only do this for builder devices! Not dev machines!
		# Add insecure pre-shared SSH public key
		ssh_insecure_public_key = util.get_file('public_key')
		os.system('echo "%s" | cat >> ~/.ssh/authorized_keys' % ssh_insecure_public_key)

def init_virtual(name=None, virtual=True):

	current_file_path = os.getcwdu()
	#cwd = os.path.join(parent_directory, '.builder', 'vagrant')

	# make "./.builder/vagrant" folder if doesn't exist
	# make "./.builder/vagrant/<vm-name>" folder for generated name
	# generate ./.builder/vagrant/<vm-name>" Vagrantfile
	#    - modify to set the name of the VM
	#    - add bootstrap.sh
	#         - run "builder init <vm-name>" on VM

	builder_folder = os.path.join(current_file_path, '.builder')
	if not os.path.exists(builder_folder):
		print 'mkdir %s' % builder_folder
		os.makedirs(builder_folder)

	vagrant_folder = os.path.join(current_file_path, '.builder', 'vagrant')
	if not os.path.exists(vagrant_folder):
		print 'mkdir %s' % vagrant_folder
		os.makedirs(vagrant_folder)

	if name == None:
		name = petname.Generate(2)
	machine_folder = os.path.join(current_file_path, '.builder', 'vagrant', name)
	if not os.path.exists(machine_folder):
		print 'mkdir %s' % machine_folder
		os.makedirs(machine_folder)
	
	# vagrant init
	vagrant_box = 'ubuntu/trusty64'
	process = subprocess.Popen(['vagrant', 'init', '-m', vagrant_box], stdout=subprocess.PIPE, cwd=machine_folder, bufsize=1)
	process.wait()

	# Generate copy of Vagrantfile from template file
	vagrantfile_data = util.get_vagrant_file(name)
	Vagrantfile = open(os.path.join(machine_folder, 'Vagrantfile'), 'w+')
	Vagrantfile.write(vagrantfile_data)
	Vagrantfile.close()

	# TODO: CLI style where you enter high level commands with minimum info to start a interactive questionairre prompting for variable values (but with defaults assigned), also skippable, and if skipped, added to "todos".

	# TODO: Hello there.
	# How are you?
	# ...
	# // this will trigger refactoring moving "TODO" on top of "Hello there". (Make a little continuous-running vim robot (scripted inline right in Vim. Make it a plugin!)).
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
	init()
