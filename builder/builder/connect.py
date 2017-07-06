import os
import re

import api
import util

def connect(requested_models):
	# Creates a YAML file describing the ports
	# Arguments:
	# --output <filename> (optional) specifies output file for port config
	#
	# Examples:
	# builder connect raspberry-pi-3 ir-rangefinder generic-servo
	# builder connect -model raspberry-pi-3 -model ir-rangefinder -model generic-servo
	# builder connect -model raspberry-pi-3 -model ir-rangefinder -model generic-servo
	#
	# Note:	The arguments are essentially shorthand for filenames that match a specific format for models.
	#       First searches local folder, then model folder, fail to asking to create it (interactively create a device on the CLI with Builder).

	model_paths = locate_model_files(requested_models)

	models = load_models(model_paths.values())

	#paths = connect_models(model_list)
	connect_models(models)

def locate_model_files(model_names):
	"""
	Accepts list of model names or model filenames.
	Returns dictionary with keys from input and values as the associated model paths.
	"""

	# Prepare and compile regular expressions to validate model identifier tokens.
	# model_path_regex = r'^[0-9a-zA-Z_-]+(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}\.(yaml)$'
	model_path_regex = r'^[0-9a-zA-Z_-]+(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}(\.(yaml)){0,1}$'
	model_path_pattern = re.compile(model_path_regex)

	# TODO: Validate requested model names. Show warning or error if invalid, and log invalid name. Then output warning/error and instruct user to inspect a log at a specified path for more information.

	print 'Requested Models:'
	for requested_model in model_names:
		is_match = model_path_pattern.match(requested_model)
		print '\t%s\t%s' % ('valid' if is_match is not None else 'invalid', requested_model)
		#print '\t%s' % requested_model
	print ''

	print 'Models Paths:'
	model_file_paths = {}
	current_dir = util.get_current_dir()
	for model_name in model_names:

		# TODO: Generate list of paths to search... rather than duplicating code!

		# Prepare and compile regular expressions for validating and identifying a model file.
		model_path_regex = r'^%s(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}\.(yaml)$' % model_name
		model_path_pattern = re.compile(model_path_regex)

		# Initialize model search process status flags
		current_dir_match = False
		library_dir_match = False
		repository_dir_match = False
		github_dir_match = False

		# Search local directory for YAML file (based on input argument)
		if current_dir_match == False:
			for file_name in util.get_file_list():
				is_match = model_path_pattern.match(file_name) is not None
				if is_match:
					current_dir_match = True
					model_file_paths[model_name] = '%s/%s' % (current_dir, file_name)

		# Search library's data/models folder
		if current_dir_match == False:
			#data_dir = util.get_data_filename('models/devices')
			data_dir = util.get_data_filename('')
			#print 'DATA_DIR:', data_dir
			for file_name in util.get_file_list(data_dir):
				is_match = model_path_pattern.match(file_name) is not None
				if is_match:
					library_dir_match = True
					model_file_paths[model_name] = '%s%s' % (data_dir, file_name) # TODO: data_dir shouldn't end in '/'

		if current_dir_match == False and library_dir_match == False:
			# TODO: Write function to load model file from a GitHub repository specified with format 'username/repo'
			None

		if current_dir_match == False and library_dir_match == False and github_dir_match == False:
			print 'No model file is available for \'%\'.' % model_name
			# TODO: Log error/warning/info
	
	for model_name in model_names:
		print '\t%s => Found model file: %s' % (model_name, model_file_paths[model_name])
	print ''
	
	return model_file_paths

def load_models(paths):
	"""
	Reads the model files located at the specified paths and returns a list of 
	model objects.
	"""
	models = []
	for path in paths:
		model = load_model(path)
		models.append(model)
	return models

def load_model(path):
	"""
	Reads and parses the model file at the specified path, instantiates a device 
	object, and returns the instantiated model.
	"""
	device = api.Device(model_path=path)
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
	#print models
	for model in models:
		print 'Port Dependencies for %s:' % model.name
		for port in model.get_ports():
			#for state in port.states:
			port_dependencies = determine_port_dependency(port)

			# TODO: search for compatible device (first look for power source (prioritized dependency satisfaction), then verify other dependencies, perserving interface consistency for multi-port interfaces)
			locate_port
		print ''
	
	print 'TODO: Generate path YAML file.'

# Locates a port on the specified model that matches the specfied port_dependency.
def locate_port(model, port_dependency):
	None

if __name__ == "__main__":
	list()
