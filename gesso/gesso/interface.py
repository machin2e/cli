import os, sys, shutil
import subprocess
import uuid
import petname
import util
import json
import collections # for OrderedDict
import logging

def add(name=None):

	# TODO: Move this into gesso.py:
	logger = util.logger('gesso')

	# Check if cwd contains .gesso, or if any of it's parents contain one (if so, we're in a gesso repository)
	#	If not, create it and populate it with a 'config' file that will contain initial config
	#	If so, print error 'Current/parent directory already contains a .gesso folder'
	sys.stdout.write('Adding interface %s.' % name)
	sys.stdout.flush()

	# TODO: Show progress bar if downloading an interface from the interface registry.

	# Initialize the gesso root file system
	gesso_root = util.get_gesso_root()
	# TODO: util.get_interface_root() --- replaces the above line, allowing nested interfaces
	interface_path = os.path.join(gesso_root, name)
	if not os.path.exists(interface_path):
		logger.info('mkdir %s' % interface_path)
		os.makedirs(interface_path)

	# Create interface configuration
	interface_config = {
		'source': 'controller.py',
		'ports': [],
		'target': 'unassigned' # the target device where the interface will be deployed
	}
	interface_config_json = json.dumps(interface_config, indent=4, sort_keys=False)
	
	interface_config_path = os.path.join(interface_path, 'interface')
	if not os.path.exists(interface_config_path):
		logger.info('touch %s' % interface_config_path)
		with open(interface_config_path, 'w+') as file:
			file.write(interface_config_json)

	# Create interface source/code
	interface_source = "import gesso\nprint gesso.api.version()\nprint \'%s\'" % name
	
	interface_source_path = os.path.join(interface_path, interface_config['source'])
	if not os.path.exists(interface_source_path):
		logger.info('touch %s' % interface_source_path)
		with open(interface_source_path, 'w+') as file:
			file.write(interface_source)
	
	sys.stdout.write(' OK.\n')
	sys.stdout.flush()

	#parent_path = util.parent_contains('.gesso')
	#if not parent_path is None:
		#print 'Error: I can\'t do that.'
		#print 'Reason: There is already a .gesso directory at %s.' % parent_path
		#print 'Hint: Use `cd` to change to a different directory.' 

def remove(name=None):

	# TODO: Move this into gesso.py:
	logger = util.logger('gesso')

	# Initialize the gesso root file system
	gesso_root = util.get_gesso_root()
	# TODO: util.get_interface_root() --- replaces the above line, allowing nested interfaces
	interface_path = os.path.join(gesso_root, name)
	if os.path.exists(interface_path):
		sys.stdout.write('Removing interface %s.' % name)
		sys.stdout.flush()

		logger.info('rm -rfd %s' % interface_path)
		shutil.rmtree(interface_path)
	
		sys.stdout.write(' OK.')
		sys.stdout.flush()

	else:
		print 'Error: I can\'t do that.'
		print 'Reason: The interface %s does not exist.' % name
		#print 'Hint: Check your spelling :).'

if __name__ == "__main__":
	init()
