# The Builderfile is used to bootstrap the Builder daemon which manages 
# the device's configuration and allows it to be edited in real-time 
# from smartphone and when plugged in over USB as mass storage.

# Create "Builderfile" that contains:
# - UUID
# - human-readable name

import os
import sys
import subprocess
import uuid
import petname

def init(name=None, virtual=False):
	if virtual == True:
		init_virtual(name, virtual)
	else:
		init_physical(name, virtual)

def init_physical(name=None, virtual=False):
	builderfile_path = './Builderfile'

	# Create default Builderfile if it doesn't exist.
	if not os.path.exists(builderfile_path):

		file = open(builderfile_path, 'w')

		# Write human-readable name
		if name == None:
			name = petname.Generate(2)
		file.write("name: %s\n" % name)

		# Write UUID
		device_uuid = uuid.uuid4()
		file.write("uuid: %s\n" % device_uuid)

		# Project UUID
		project_uuid = None
		file.write("project: %s\n" % project_uuid)

		# Provider: builder, vagrant

		file.close()

	else:
		# Read the Builderfile
		# TODO: Initialize the daemon here?
		file = open(builderfile_path, 'r')
		filelines = file.readlines()

		for i in range(len(filelines)):

			# Read human-readable name 
			if filelines[i].startswith('name:'):
				name = filelines[i].split(': ')[1]
				#print filelines[i]
				print name.replace('\n', '')

			# Read UUID
			if filelines[i].startswith('uuid:'):
				device_uuid = filelines[i].split(': ')[1]
				#print filelines[i]
				print device_uuid.replace('\n', '')

			# Read Project UUID
			if filelines[i].startswith('project:'):
				device_uuid = filelines[i].split(': ')[1]
				#print filelines[i]
				print device_uuid.replace('\n', '')

		file.close()

def init_virtual(name=None, virtual=True):

	#cwd = os.path.dirname(os.path.realpath(__file__))
	#cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.builder', 'vagrant')
	#current_file_path = os.path.abspath(__file__)
	current_file_path = os.getcwdu()
	current_directory = os.path.abspath(os.path.join(current_file_path, os.pardir)) # this will return current directory in which python file resides.
	parent_directory  = os.path.abspath(os.path.join(current_directory, os.pardir)) 
	#cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.builder', 'vagrant')
	cwd = os.path.join(parent_directory, '.builder', 'vagrant')
	print cwd

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

	# Generate Vagrantfile
	Vagrantfile = open(os.path.join(machine_folder, 'Vagrantfile'))
	file_lines = Vagrantfile.readlines()
	Vagrantfile.close()
	file_lines.insert(2, '  config.vm.provider "virtualbox" do |v|\n'); # machine name
	file_lines.insert(3, '    v.name = "%s"\n' % name);
	file_lines.insert(4, '  end\n');
	file_lines.insert(5, '  config.vm.network "public_network"\n') # network
	file_lines.insert(6, '  config.vm.synced_folder "../../../%s", "/builder"\n' % name) # device sync dir (TODO: use rsync, not vagrant)
	file_lines.insert(7, '  config.vm.provision "shell", inline: "apt -y install git python-pip"') # device sync dir (TODO: use rsync, not vagrant)
	#file_lines.insert(6, '  config.vm.synced_folder "../../../builder", "/builder/builder"\n') # builder CLI (should use git or package manager)

	#file_lines.insert(6, '  config.vm.synced_folder "../../../%s", "/builder"\n' % name) # synced folder
	#file_lines.insert(7, '  config.vm.synced_folder "../../../builder", "/builder/builder", type: "rsync", rsync__args: ["--include=../../../builder.py"]\n')
	Vagrantfile = open(os.path.join(machine_folder, 'Vagrantfile'), 'w')
	Vagrantfile.writelines(file_lines)
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

def vagrant_status():
	cwd = os.path.dirname(os.path.realpath(__file__))
	cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.builder', 'vagrant')

	curfilePath = os.path.abspath(__file__)
	curDir = os.path.abspath(os.path.join(curfilePath,os.pardir)) # this will return current directory in which python file resides.
	parentDir = os.path.abspath(os.path.join(curDir,os.pardir)) 
	#cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.builder', 'vagrant')
	cwd = os.path.join(parentDir, '.builder', 'vagrant')
	print cwd

	process = subprocess.Popen(['vagrant', 'status'], stdout=subprocess.PIPE, cwd=cwd, bufsize=1)

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
