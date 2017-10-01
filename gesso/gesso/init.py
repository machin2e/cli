import os, sys
import subprocess
import uuid
import petname
import util
import json
import collections # for OrderedDict

def init(name=None, role='workspace'):

	# Check if cwd contains .gesso, or if any of it's parents contain one (if so, we're in a gesso repository)
	#	If not, create it and populate it with a 'config' file that will contain initial config
	#	If so, print error 'Current/parent directory already contains a .gesso folder'

	parent_path = util.parent_contains('.gesso')
	if not parent_path is None:
		print 'Error: I can\'t do that.'
		print 'Reason: There is already a .gesso directory at %s.' % parent_path
		print 'Hint: Use `cd` to change to a different directory.' 

	else:

		gesso_root = os.getcwdu()

		# Initialize the gesso root file system
		gesso_path = os.path.join(gesso_root, '.gesso')
		if not os.path.exists(gesso_path):
			print 'mkdir %s' % gesso_path 
			os.makedirs(gesso_path)

		# Initialize gesso config file
		#gesso_config = collections.OrderedDict()
		#gesso_config['name'] = petname.Generate(2) if name == None else name
		#gesso_config['uuid'] = str(uuid.uuid4()) # TODO: Read UUID from device via Gesso API
		#gesso_config['role'] = str(role)
		#gesso_config['project'] = 'none'
		gesso_config = {
			'name': petname.Generate(2) if name == None else name,
			'uuid': str(uuid.uuid4()), # TODO: read UUID from hardware!
			'role': str(role),
			'project': 'none'
		}
		gesso_config_json = json.dumps(gesso_config, indent=4, sort_keys=False)

		gesso_config_path = os.path.join(gesso_root, '.gesso', 'config')
		if not os.path.exists(gesso_config_path):
			print 'touch %s' % gesso_config_path 
			with open(gesso_config_path, 'w+') as file:
				file.write(gesso_config_json)

		# create interface configuration
		system_controller_source = 'import gesso\nimport gesso.api\nprint gesso.api.version()'
		
		system_controller_path = os.path.join(gesso_root, 'system.py')
		if not os.path.exists(system_controller_path):
			logger.info('touch %s' % system_controller_path)
			with open(system_controller_path, 'w+') as file:
				file.write(system_controller_source)

		# gesso init zesty-koala --virtual
		if role == 'gesso':
			# This is done only gesso devices. Not dev machines!
			# Add insecure pre-shared SSH public key (to boostrap communications)
			insecure_ssh_public_key = util.get_file('public_key')
			os.system('echo "%s" | cat >> ~/.ssh/authorized_keys' % insecure_ssh_public_key)
		elif role == 'workspace':
			insecure_ssh_private_key = util.get_data_filename('private_key')
			os.system('ssh-add %s' % insecure_ssh_private_key)

if __name__ == "__main__":
	init()
