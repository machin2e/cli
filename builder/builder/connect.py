import os
import re

import api
import util

def connect(models):
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

	print 'Models:'
	model_paths = {}
	for model in models:

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
	model_list = []
	for model in models:
		model_path = model_paths[model]
		device = open_model(model_path)
		model_list.append(device)

	connect_models(model_list)
	return

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
	
	print 'TODO: Generate path YAML file.'

# Locates a port on the specified model that matches the specfied port_dependency.
def locate_port(model, port_dependency):
	None

if __name__ == "__main__":
	list()
