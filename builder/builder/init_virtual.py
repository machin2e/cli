import subprocess
import os
import sys
import petname

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
	init_virtual()
