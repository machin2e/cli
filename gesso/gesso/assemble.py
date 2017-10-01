import os
import re
import logging

import api
import git
import util

def assemble(component_identifiers):
	"""
	Creates a YAML file describing the ports
	Arguments:
	--output <filename> (optional) specifies output file for port config
	
	Examples:
	gesso assemble raspberry-pi-3 ir-rangefinder generic-servo
	gesso assemble --component raspberry-pi-3 --component ir-rangefinder --component generic-servo
	gesso assemble --component raspberry-pi-3 --component ir-rangefinder --component generic-servo
	
	Note:	The arguments are essentially shorthand for filenames that match a specific format for models.
		  First searches local folder, then model folder, fail to asking to create it (interactively create a device on the CLI with Builder).
	"""

	component_paths = find_component_files(component_identifiers)
	components = load_components(component_paths.values())
	paths = assemble_components(components)

def find_component_files(component_identifiers):
	"""
	Accepts list of component identifiers (such as names), filenames, GitHub 
	repositories (e.g., "machineee/raspberry-pi-3"), or file paths.

	Returns dictionary with keys from input and values as the associated 
	component paths.
	"""

	# Prepare and compile regular expressions to validate model identifier tokens.
	# Matches strings such as:
	# - without semantic version: "gesso", "arduino", "raspberry-pi-3
	# - with semantic version: "gesso-3", "gesso-3.0", "gesso-3.0.0"
	generic_component_identifier_pattern = re.compile(r'^[0-9a-zA-Z_-]+(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}(\.(yaml)){0,1}$')

	# Matches strings such as:
	# - "machineee/ir-rangefinder"
	# - "machineee/raspberry-pi-3"
	component_github_pattern = re.compile(r'^[A-Za-z0-9-_]+\/[A-Za-z0-9-_]+$')

	# Validate the requested component identifiers. Halt and show error if 
	# any are not in a valid format.
	print 'Requested components (by identifier):'
	for component_identifier in component_identifiers:
		is_match = generic_component_identifier_pattern.match(component_identifier)
		print '\t%s\t%s' % ('valid' if is_match is not None else 'invalid', component_identifier)
	print ''

	print 'Component File Paths:'
	component_file_paths = {}
	current_dir = util.get_current_dir()
	for component_identifier in component_identifiers:

		# Prepare and compile regular expressions for validating and identifying a model file.
		component_path_pattern = re.compile(r'^%s(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}\.(yaml)$' % component_identifier)

		# Search local directory for YAML file (based on input argument)
		if component_identifier not in component_file_paths:
			for file_name in util.get_file_list():
				if component_path_pattern.match(file_name) is not None:
					component_file_paths[component_identifier] = '%s/%s' % (current_dir, file_name)

		# Search library's data/models folder
		if component_identifier not in component_file_paths:
			data_dir = util.get_data_dir()
			for file_name in util.get_file_list(data_dir):
				if component_path_pattern.match(file_name) is not None:
					component_file_paths[component_identifier] = '%s/%s' % (data_dir, file_name) # TODO: data_dir shouldn't end in '/'

		# Check for GitHub repository identifier
		if component_identifier not in component_file_paths:
			# TODO: Write function to load model file from a GitHub repository specified with format 'username/repo'
			if component_github_pattern.match(component_identifier) is not None:
				print('Cloning %s/%s to %s/%s/%s' % (username, repository, '.gesso/components', username, repository))
				username, repository = component_identifier.split('/')
				git.clone_github_repository(username, repository)

		# No component file was found for the specified identifer, so halt and show an error.
		if component_identifier not in component_file_paths:
			print "No component file found for '%s'." % component_identifier 
			# TODO: Log error/warning/info
			None
	
	for component_identifier in component_identifiers:
		print '\t%s => Found component file: %s' % (component_identifier, component_file_paths[component_identifier])
	print ''
	
	return component_file_paths 

def load_components(paths):
	"""
	Reads the model files located at the specified paths and returns a list of 
	model objects.
	"""
	components = []
	for path in paths:
		component = api.Component(path=path)
		components.append(component)
	return components

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


# TODO: expand state combinatorics and check each of them... to allow connecting two Builders, for example...


	for state2 in port.states:

		state_list = determine_state_list(state2)

		for state in state_list:

			# port_dependency = {
					# 'mode': [],
					# 'direction': [],
					# 'voltage': []
			# }

			port_dependency = {
					'mode': None,
					'direction': None,
					'voltage': None
			}

			# Determine mode compatibility
			# TODO: iterate through all available elements of array (for devices like Pi that have multiple states/configs per port)
			# TODO: change 'mode' to 'role' OR 'function', 'service', 'purpose'?
			if 'power' == state['mode']:
				port_dependency['mode'] = 'power'
			elif 'digital' == state['mode']:
				port_dependency['mode'] = 'digital'
			elif 'analog' == state['mode']: # adc?
				port_dependency['mode'] = 'analog'
			elif 'resistive-touch' == state['mode']:
				port_dependency['mode'] = 'resistive-touch'
			elif 'pulse-width-modulation' == state['mode']:
				port_dependency['mode'] = 'pulse-width-modulation' # alt: PWM, pwm
			elif 'i2c(scl)' == state['mode']: # alt: I2C(SCL)
				port_dependency['mode'] = 'i2c(scl)'
			elif 'i2c(sda)' == state['mode']: # alt: I2C(SDA)
				port_dependency['mode'] = 'i2c(sda)'
			elif 'spi(sclk)' == state['mode']:
				port_dependency['mode'] = 'spi(sclk)'
			elif 'spi(mosi)' == state['mode']:
				port_dependency['mode'] = 'spi(mosi)'
			elif 'spi(miso)' == state['mode']:
				port_dependency['mode'] = 'spi(miso)'
			elif 'spi(ss)' == state['mode']:
				port_dependency['mode'] = 'spi(ss)'
			elif 'uart(tx)' == state['mode']:
				port_dependency['mode'] = 'uart(rx)'
			elif 'uart(rx)' == state['mode']:
				port_dependency['mode'] = 'uart(tx)'

			# Determine direction compatibility
			# TODO: Double-check this logic... it's not complete!
			if 'input' == state['direction']:
				port_dependency['direction'] = 'output'
			elif 'output' == state['direction']:
				port_dependency['direction'] = 'input'
			elif 'bidirectional' == state['direction']:
				port_dependency['direction'] = 'bidirectional'

			# Determine power compatibility
			# TODO: Support voltage ranges! e.g., [3.3v, 5v]
			if '3.3v' == state['voltage']:
				port_dependency['voltage'] = '3.3v'
			elif '5v' == state['voltage']:
				port_dependency['voltage'] = '5v'
			elif '0v' == state['voltage']:
				port_dependency['voltage'] = '0v'

			# # Determine mode compatibility
			# # TODO: iterate through all available elements of array (for devices like Pi that have multiple states/configs per port)
			# # TODO: change 'mode' to 'role' OR 'function', 'service', 'purpose'?
			# if 'power' in state['mode']:
				# port_dependency['mode'].append('power')
			# elif 'digital' in state['mode']:
				# port_dependency['mode'].append('digital')
			# elif 'analog' in state['mode']: # adc?
				# port_dependency['mode'].append('analog')
			# elif 'resistive-touch' in state['mode']:
				# port_dependency['mode'].append('resistive-touch')
			# elif 'pulse-width-modulation' in state['mode']:
				# port_dependency['mode'].append('pulse-width-modulation') # alt: PWM, pwm
			# elif 'i2c(scl)' in state['mode']: # alt: I2C(SCL)
				# port_dependency['mode'].append('i2c(scl)')
			# elif 'i2c(sda)' in state['mode']: # alt: I2C(SDA)
				# port_dependency['mode'].append('i2c(sda)')
			# elif 'spi(sclk)' in state['mode']:
				# port_dependency['mode'].append('spi(sclk)')
			# elif 'spi(mosi)' in state['mode']:
				# port_dependency['mode'].append('spi(mosi)')
			# elif 'spi(miso)' in state['mode']:
				# port_dependency['mode'].append('spi(miso)')
			# elif 'spi(ss)' == state['mode']:
				# port_dependency['mode'].append('spi(ss)')
			# elif 'uart(tx)' in state['mode']:
				# port_dependency['mode'].append('uart(rx)')
			# elif 'uart(rx)' in state['mode']:
				# port_dependency['mode'].append('uart(tx)')

			# # Determine direction compatibility
			# # TODO: Double-check this logic... it's not complete!
			# if 'input' in state['direction']:
				# port_dependency['direction'].append('output')
			# elif 'output' in state['direction']:
				# port_dependency['direction'].append('input')
			# elif 'bidirectional' in state['direction']:
				# port_dependency['direction'].append('bidirectional')

			# # Determine power compatibility
			# # TODO: Support voltage ranges! e.g., [3.3v, 5v]
			# if '3.3v' in state['voltage']:
				# port_dependency['voltage'].append('3.3v')
			# elif '5v' in state['voltage']:
				# port_dependency['voltage'].append('5v')
			# elif '0v' in state['voltage']:
				# port_dependency['voltage'].append('0v')

			# TODO: verify validity before adding to dependency/compatibility list
			port_dependencies.append(port_dependency)
	
	print '\t%s' % port_dependencies

	return port_dependencies

# TODO: integrate with determine_port_dependencies(port) and rename to determine_dependencies(...) and check type to determine functionality
def determine_device_port_dependencies(model):
	port_dependencies = { 'ports': {} }
	print 'Port Dependencies for %s:' % model.name
	for port in model.get_ports():
		port_dependency = determine_port_dependency(port)
		port_dependencies['ports'][port] = port_dependency
	print ''
	return port_dependencies

# TODO: test_device_compatibility(device, device)
# TODO?: connect_devices(model, model)
def assemble_components(models):
	"""
	Determines whether the models can be connected or not.
	If they can be connected, it searches for valid connections.
	If a complete, valid set of connections is found, the connections are returned.
	(The returned connections are used to describe step by step connections + chart.)
	(The returned connections are written to a file.)
	"""

	# route(models)
	# Pseudocode:
	# Start with devices that have _only_ a single configuration per port.
	# - seek power sources
	# - for a found power source, check if the source also satisfies the other dependencies
		# - if so, find connections on the device
		# - if not, continue to next power source candidate...


	# TODO: Infer hosts or ask user interactively or store in YAML file
	hosts = ['Raspberry Pi 3']



	paths = []

	port_dependencies = {}
	for model in models:
		port_dependencies[model] = determine_device_port_dependencies(model)
		# port_dependencies[model] = { 'ports': {} }
		# print 'Port Dependencies for %s:' % model.name
		# for port in model.get_ports():
			# port_dependency = determine_port_dependency(port)
			# port_dependencies[model]['ports'][port] = port_dependency
		# print ''

	for model in models:

		if model.name in hosts:
			print 'Skipping compatibility search for host %s.' % model.name
			print ''
			continue

		print 'Searching for compatible ports for %s:' % model.name
		for port in model.get_ports():
			# TODO: search for compatible device (first look for power source (prioritized dependency satisfaction), then verify other dependencies, perserving interface consistency for multi-port interfaces)
			port_dependency = port_dependencies[model]['ports'][port]
			compatible_ports = locate_compatible_port(model, port, port_dependency, models)
			
			# Generate list of compatible paths
			# TODO: Make sure all required information is stored...
			for compatible_port in compatible_ports:
				path = api.Path()
				path.ports.append(port)
				path.ports.append(compatible_port)

				paths.append(path)

		print ''
	
	print 'AVAILABLE PATHS:'
	for path in paths:
		print path
	
	# TODO: Generate list of valid paths.

	print 'TODO: Generate step-by-step instructions. Update connections on the fly as connections are made? Sure, but add option for automating.'
	
	print 'TODO: Generate path YAML file.'

# TODO?: change to determine_state_list(port)
def determine_state_list(state):
	# Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
	# Search through ALL possible combination pairs for all mode,direction,voltage combos on ports... and store list of possibilities!
	port_configuration_list = [] # TODO: compute these...
	for mode in state['mode']:
		for direction in state['direction']:
			for voltage in state['voltage']:
				port_configuration_list.append({ 'mode': mode, 'direction': direction, 'voltage': voltage })
	return port_configuration_list

# TODO: locate_compatible_interface(...)
def locate_compatible_port(source_device, source_port, source_port_dependencies, devices):
	"""
	Locates a port on the specified model that matches the specfied port_dependency.
	todo: parallelize this function... so many nested loops!
	"""
	print '\tPort %s on %s:' % (source_port.number, source_device.name)
	print '\t\tStates: %s' % source_port.states 
	print '\t\tDependencies: %s' % source_port_dependencies

	compatible_port_list = {}
	# compatible_port_list[other_device] = []
	# compatible_port_list[other_device]['port'] = []
	# compatible_port_list[other_device]['state'] = []
	for device in devices:

		# Prevent attempt to search for compatible ports on the same device
		# TODO: Add option to enable searching on the same device
		# if device == source_device:
			# continue

		# Initialize storage for compatible ports on other device
		compatible_port_list[device] = {}

		# print 'Port Dependencies for %s:' % model.name
		for port in device.ports:

			for state in port.states:

				# Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
				# Search through ALL possible combination pairs for all mode,direction,voltage combos on ports... and store list of possibilities!
				# TODO: expand this state sooner? or use cached computation?
				port_configuration_list = determine_state_list(state)

				# Determine compatible ports
				for port_dependency in source_port_dependencies:
					for port_configuration in port_configuration_list:
						if port_configuration['mode'] == port_dependency['mode'] and port_configuration['direction'] == port_dependency['direction'] and port_configuration['voltage'] == port_dependency['voltage']:

							# Just-in-time initialize storage for compatible port states on other device's port to empty list
							if not port in compatible_port_list[device]:
								compatible_port_list[device][port] = []

							compatible_port_list[device][port].append({ 'port': port, 'state': port_configuration })

	# Print the compatible ports (if any).
	# For devices that provide no compatible ports, print 'None'.
	print '\t\tCompatible Ports:'
	for device in compatible_port_list:

		if len(compatible_port_list[device]) == 0:
			print '\t\t\t%s: None' % device.name
		else:
			print '\t\t\t%s:' % device.name

		for port in compatible_port_list[device]:
			print '\t\t\t\tPort %s:' % port.number
			for compatible_port in compatible_port_list[device][port]:
				print '\t\t\t\t\t%s, %s, %s' % (compatible_port['state']['mode'], compatible_port['state']['direction'], compatible_port['state']['voltage'])

	return compatible_port_list 

def select_compatible_port(port, compatible_port_list):
	"""
	Selects a port from `compatible_port_list` to which `port` will be connected with a path.
	"""
	None

if __name__ == "__main__":
	assemble()
