#!/usr/bin/env python

from imports import *
import argparse
import api
import util
import re

import os

def open_model(path):
	device = api.Device(model_path=path)
	#for port in device.get_ports():
		#for state in port.states:
			#print state.mode
			#print state.direction
			#print state.voltage
			#print state['mode']
			#print state['direction']
			#print state['voltage']
	#print port.states
	return device

def determine_state_compatability(state):
	return None

# Determines the requirements for connecting to the specified port.
# Used in the interactive self-assembly process for generating port connections.
def determine_port_dependency(port):
	#return 'requirement: %s' % port
	port_dependencies = []
	#for state in port.states:
	#	print state
	
	# TODO: determine_compatible_interfaces(arduino, arduino)

	for state in port.states:

		port_dependency = {
				'mode': [],
				'direction': [],
				'voltage': []
		}

		# Determine mode compatibility
		# TODO: iterate through all available elements of array (for devices like Pi that have multiple states/configs per port)
		# TODO: change 'mode' to 'role' OR 'function', 'service', 'purpose'?
		if 'power' in state['mode']:
			port_dependency['mode'].append('power')
		elif 'digital' in state['mode']:
			port_dependency['mode'].append('digital')
		elif 'analog' in state['mode']: # adc?
			port_dependency['mode'].append('analog')
		elif 'resistive-touch' in state['mode']:
			port_dependency['mode'].append('resistive-touch')
		elif 'pulse-width-modulation' in state['mode']:
			port_dependency['mode'].append('pulse-width-modulation') # alt: PWM, pwm
		elif 'i2c(scl)' in state['mode']: # alt: I2C(SCL)
			port_dependency['mode'].append('i2c(scl)')
		elif 'i2c(sda)' in state['mode']: # alt: I2C(SDA)
			port_dependency['mode'].append('i2c(sda)')
		elif 'spi(sclk)' in state['mode']:
			port_dependency['mode'].append('spi(sclk)')
		elif 'spi(mosi)' in state['mode']:
			port_dependency['mode'].append('spi(mosi)')
		elif 'spi(miso)' in state['mode']:
			port_dependency['mode'].append('spi(miso)')
		elif 'spi(ss)' == state['mode']:
			port_dependency['mode'].append('spi(ss)')
		elif 'uart(tx)' in state['mode']:
			port_dependency['mode'].append('uart(rx)')
		elif 'uart(rx)' in state['mode']:
			port_dependency['mode'].append('uart(tx)')

		# Determine direction compatibility
		# TODO: Double-check this logic... it's not complete!
		if 'input' in state['direction']:
			port_dependency['direction'].append('output')
		elif 'output' in state['direction']:
			port_dependency['direction'].append('input')
		elif 'bidirectional' in state['direction']:
			port_dependency['direction'].append('bidirectional')

		# Determine power compatibility
		# TODO: Support voltage ranges! e.g., [3.3v, 5v]
		if '3.3v' in state['voltage']:
			port_dependency['voltage'].append('3.3v')
		elif '5v' in state['voltage']:
			port_dependency['voltage'].append('5v')
		elif '0v' in state['voltage']:
			port_dependency['voltage'].append('0v')

		# TODO: verify validity before adding to dependency/compatibility list
		port_dependencies.append(port_dependency)
	
	print '\t%s' % port_dependencies

# route(models)
# Pseudocode:
# - seek power sources
#   - for a found power source, check if the source also satisfies the other dependencies
#     - if so, find connections on the device
#     - if not, continue to next power source candidate...
def connect_models(models):
	"""
	Determines whether the models can be connected or not.
	If they can be connected, it searches for valid connections.
	If a complete, valid set of connections is found, the connections are returned.
	(The returned connections are used to describe step by step connections + chart.)
	(The returned connections are written to a file.)
	"""
	port_dependencies = {}
	print models
	for model in models:
		print 'DEPENDENCIES FOR %s:' % model.name
		for port in model.get_ports():
			#for state in port.states:
			port_dependencies = determine_port_dependency(port)

			# TODO: search for compatible device (first look for power source (prioritized dependency satisfaction), then verify other dependencies, perserving interface consistency for multi-port interfaces)
			locate_port 

# Locates a port on the specified model that matches the specfied port_dependency.
def locate_port(model, port_dependency):
	None

def builder(command=None):

	# Define command-line argument parser
	parser = argparse.ArgumentParser(description='Builder command-line interpreter.')
	parser.add_argument('command')
	parser.add_argument('option1', nargs='?', default=None)
	parser.add_argument('option2', nargs='?', default=None)
	# TODO: Make these optional arguments only show up for relevant argument trees.
	parser.add_argument('-v', '--virtual', action='store_true', help='specify virtual machine (use with init)')
	parser.add_argument('-r', '--role', default='workspace', choices=['workspace','builder'], help='specify role of builder context (use with init)')
	parser.add_argument('--model', action='append', dest='models', nargs='?', default=[], help='Add models for command.')

	# Parse arguments
	args = None
	if not command == None:
		myargs = command.split(' ')
		args = parser.parse_args(myargs)
	else:
		args = parser.parse_args()

	# TODO: Search for all available "builder_*" files in toolchain and print error with command to repair the toolchain.
	

	if not args.command == 'init':
		if not util.is_builder_tree():
			print 'Error: I can\'t do that.'
			print 'Reason: There is no .builder directory in the current or parent directories.'
			print 'Hint: Run `builder init`.' 
			return

	# TODO: make sure `builder init` was called prior to other commands!

	# TODO: during `builder init`, load device .yaml files into memory! then can set state and push to device (and sync, eventually)
	# TODO: don't worry about filesystem too much for now... just load model (proxy for download), then update state through API... DO THIS IN CONTROLLER? NOT CLI? PROBALBY!!!!!!!
	if args.command == 'port':
		#path = os.path.join(util.get_builder_root(), '_robot', 'motors', 'right-servo', 'model-device-builder.yaml')
		path = os.path.join(util.get_builder_root(), '.builder', 'devices', 'builder-8.0.0.yaml')
		device = api.Device(model_path=path)
		for port in device.get_ports():
			print port.mode
			print port.direction
			print port.voltage
		print port.states
	
	elif args.command == 'connect':
		# Creates a YAML file describing the ports
		# Arguments:
		# --output <filename> (optional) specifies output file for port config
		#
		# Examples:
		# builder connect raspberry-pi-3 ir-rangefinder generic-servo
		# builder connect -model raspberry-pi-3 -model ir-rangefinder -model generic-servo
		# builder connect -model raspberry-pi-3 -model ir-rangefinder -model generic-servo
		#
		# Note:	The arguments refer to model file names. First search local folder, then model folder, fail to asking to create it (interactively create a device on the CLI with Builder).

		model_path_regex = r'^[0-9a-zA-Z_-]+(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}\.(yaml)$'
		model_path_pattern = re.compile(model_path_regex)

		#print args.model
		print 'Models:'
		model_paths = {}
		for model in args.models:

			# TODO: search local directory for yaml file (based on input argument)
			# TODO: search data/models folder


			file_names = util.get_file_list()
			#print file_names


			model_path = '%s-x.x.x.yaml' % model
			#print '- %s\t%s' % (model, model_path)



			current_dir = util.get_current_dir()
			has_model_file = util.contains_file(current_dir, model_path)



			current_dir_match = False
			registry_dir_match = False

			if current_dir_match == False:
				for file_name in util.get_file_list():
					#is_match = model_path_pattern.match(model_path)
					is_match = file_name.startswith(model)
					if is_match:
						print '\tFound in currect directory: %s' % file_name
						current_dir_match = True
						model_paths[model] = '%s/%s' % (current_dir, file_name)

			if current_dir_match == False:
				#data_dir = util.get_data_filename('models/devices')
				data_dir = util.get_data_filename('')
				#print 'DATA_DIR:', data_dir
				for file_name in util.get_file_list(data_dir):
					#print "FILE: %s" % file_name
					#is_match = model_path_pattern.match(model_path)
					is_match = file_name.startswith(model)
					if is_match:
						print '\tFound in registry: %s' % file_name
						registry_dir_match = True
						model_paths[model] = '%s%s' % (data_dir, file_name) # TODO: data_dir shouldn't end in '/'
						
		print 'model_paths dict:'
		models = []
		for model in args.models:
			model_path = model_paths[model]
			device = open_model(model_path)
			models.append(device)

		connect_models(models)
		return


	if args.command == "init":
		init(name=args.option1, role=args.role)

	elif args.command == 'status':
		# TODO: Print current status. Ex: 'running', 'paused', 'stopped'
		None	

	elif args.command == "start":

		print '▒█▀▀█ ▒█░▒█ ▀█▀ ▒█░░░ ▒█▀▀▄ ▒█▀▀▀ ▒█▀▀█ '
		print '▒█▀▀▄ ▒█░▒█ ▒█░ ▒█░░░ ▒█░▒█ ▒█▀▀▀ ▒█▄▄▀ '
		print '▒█▄▄█ ░▀▄▄▀ ▄█▄ ▒█▄▄█ ▒█▄▄▀ ▒█▄▄▄ ▒█░▒█ '

		# TODO: for hosts, load their own device file, and the device files for connected peripherals, their controllers, etc.; init in-memory state of board

		service.manage.start()
		service.announce.start()
	elif args.command == "pause":
		service.manage.stop()
		service.announce.stop()
		# TODO: Suspend VMs! `vagrant suspend` (Y/N)
	elif args.command == "resume":
		service.manage.start()
		service.announce.start()
		# TODO: Resume VMs! `vagrant resume` (if suspended)
	elif args.command == "stop":
		service.manage.stop()
		service.announce.stop()
		# TODO: Start VMs! `vagrant suspend`
	elif args.command == 'announce':
		if args.option1 == 'start':
			service.announce.start()
		elif args.option1 == 'run':
			service.announce.run()
		elif args.option1 == 'stop':
			service.announce.stop()
	elif args.command == 'manage':
		if args.option1 == 'start':
			service.manage.start()
		elif args.option1 == 'run':
			service.manage.run()
		elif args.option1 == 'stop':
			service.manage.stop()
	elif args.command == 'monitor':
		if args.option1 == 'start':
			None
		elif args.option1 == 'run':
			service.watchdir.run()
		elif args.option1 == 'stop':
			None
	

	elif args.command == 'project': # app
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'device':
		if args.option1 == 'list':
			device.list(args.option2)
		elif args.option1 == 'search':
			# TODO: Search device registry for a device name/description matching specified string/regex
			None
		elif args.option1 == 'add':
			device.add(args.option2, virtual=args.virtual)
		elif args.option1 == 'start':
			device.start(args.option2)
		elif args.option1 == 'ssh':
			device.ssh(args.option2)
		elif args.option1 == 'restart':
			device.restart(args.option2)
		elif args.option1 == 'pause':
			device.pause(args.option2)
		elif args.option1 == 'stop':
			device.stop(args.option2)
		elif args.option1 == 'remove':
			device.remove(args.option2)
	elif args.command == 'interface':
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			interface.add(args.option2)
		elif args.option1 == 'remove':
			interface.remove(args.option2)
		elif args.option1 == 'compose':
			# TODO: Composes multiple interfaces under a new interface. Generates interface file with dependencies.
			None
	elif args.command == 'controller': # logic
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'view':
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'material': # Alt: 'design', 'asset' (CAD design file)
		None

	# builder port add digital,output,ttl --interface servo
	# builder port add digital,output,ttl --interface servo
	# builder port add digital,output,ttl --interface servo

	# builder interface deploy|assign <device-name>

	# builder interface assemble|install

	# builder assemble|install

	# builder deploy

	elif args.command == 'log':
		# TODO: builder [device <name>] log <announce|manage|command>
		None

	elif args.command == 'sync':
		sync(args.option1)

	elif args.command == 'login':
		None
	elif args.command == 'logout':
		None
	elif args.command == 'signup':
		None
	elif args.command == 'whoami':
		None
	elif args.command == "clean":
		clean()

	elif args.command == "version":
		api.version()
	
	else:
		print 'Error: I can\'t do that.'
		print 'Reason: Unrecognized expression.'
		print 'Hint: Run `builder help` to see what I can do.'

# TODO: INCORPORATE UDP I/O (LIKE ECHO) INTO LIST TO RETURN STRINGS FROM DEVICES. MAKE "listing" A PARAMETER IN DEVICE Builderfile. / "sync" (if not list): CREATES FOLDERS ON LOCAL SYSTEM FOR DISCOVERED DEVICES (ADD-ONLY UNLESS COMMAND TO CLEANUP/REBASE) WITH SYNC FOLDERS.
# TODO: COMMAND-LINE IASM. START WITH COMMAND ON A HOST/DEVICE: ./builder interface add mokogobo/ir-rangefinder ; THEN IT DOWNLOADS THE CONFIG FOR THE FILE, ASKS WHICH PINS TO USE (OR AUTO-SELECT, BASED ON INTERNAL STATE), THEN GIVES YOU ON-SCREEN INSTRUCTIONS TO ASSEMBLE/EDIT STATE.
# "IT'S ACTUALLY FUN TO PROGRAM BY JUMPING AROUND SEEING THE HIGHLIGHTED DEVICE SO YOU KNOW WHERE YOU'RE WORKING, AND SEEING HUD ON PHONE AND IN WINDOWS ON DESKTOP (SUMMONABLE/ASSIGNABLE VIA COMMAND LINE. SHOW UP AS SNAPPABLE WINDOWS. CAN SAVE AND CHANGE VIEWS WITH A COMMAND AS WELL. CAN MAKE ALWAYS ON TOP, TOO.).

if __name__ == "__main__":
	builder()
