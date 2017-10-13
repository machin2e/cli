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

	Note:
        The arguments are essentially shorthand for filenames that match a specific format for models.
        First searches local folder, then model folder, fail to asking to create it (interactively create a device on the CLI with Builder).
	"""

	logger = util.logger(__name__)

	logger.info('%s' % component_identifiers)
        # print component_identifiers

	component_paths = find_component_files(component_identifiers)
	# components = api.Component.open(component_paths.values())
	logger.info('%s' % component_paths)
        # print component_paths

	components = api.Component.open(component_paths)
	logger.info('%s' % components)
        # print components

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
		if generic_component_identifier_pattern.match(component_identifier) or component_github_pattern.match(component_identifier):
			print '\tvalid\t%s' % component_identifier
		else:
			print '\tinvalid\t%s' % component_identifier
	print ''

	print 'Component File Paths:'
	component_file_paths = {}
        path_list = []
	current_dir = util.get_current_dir()
	for component_identifier in component_identifiers:

		# Prepare and compile regular expressions for validating and identifying a model file.
		component_path_pattern = re.compile(r'^%s(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}\.(yaml)$' % component_identifier)

		# Search local directory for YAML file (based on input argument)
		# if component_identifier not in component_file_paths:
                for file_name in util.get_file_list():
                        if component_path_pattern.match(file_name) is not None:
                                component_file_paths[component_identifier] = '%s/%s' % (current_dir, file_name)
                                path_list.append('%s/%s' % (current_dir, file_name))

		# Search library's data/models folder
		# if component_identifier not in component_file_paths:
                data_dir = util.get_data_dir()
                for file_name in util.get_file_list(data_dir):
                        if component_path_pattern.match(file_name) is not None:
                                component_file_paths[component_identifier] = '%s/%s' % (data_dir, file_name) # TODO: data_dir shouldn't end in '/'
                                path_list.append('%s/%s' % (data_dir, file_name))

		# Check for GitHub repository identifier
		# if component_identifier not in component_file_paths:
			# TODO: Write function to load model file from a GitHub repository specified with format 'username/repo'
                if component_github_pattern.match(component_identifier) is not None:
                        print('Cloning %s/%s to %s/%s/%s' % (username, repository, '.gesso/components', username, repository))
                        username, repository = component_identifier.split('/')
                        git.clone_github_repository(username, repository)

		# No component file was found for the specified identifer, so halt and show an error.
		# if component_identifier not in component_file_paths:
                    # print "No component file found for '%s'." % component_identifier
                    # # TODO: Log error/warning/info
                    # None

	for component_identifier in component_identifiers:
		print '\t%s => Found component file: %s' % (component_identifier, component_file_paths[component_identifier])
	print ''

	return path_list
	# return component_file_paths

def assemble_components(components):
	"""
	Determines whether the components can be connected or not.
	If they can be connected, it searches for valid connections.
	If a complete, valid set of connections is found, the connections are returned.
	(The returned connections are used to describe step by step connections + chart.)
	(The returned connections are written to a file.)
	"""

        system = api.System()
        system.components.extend(components)

	# route(components)
	# Pseudocode:
	# Start with devices that have _only_ a single configuration per port.
	# - seek power sources
	# - for a found power source, check if the source also satisfies the other dependencies
		# - if so, find connections on the device
		# - if not, continue to next power source candidate...


	# TODO: Infer hosts or ask user interactively or store in YAML file
	hosts = ['Raspberry Pi 3']



	paths = []

	for component in system.components:

		if component.name in hosts:
			print 'Skipping compatibility search for host %s.\n' % component.name
			continue

		# print 'Searching for compatible ports for %s:' % component.name
		print "Let's connect the <%s>." % component.name
		for port in component.ports:
			# TODO: search for compatible device (first look for power source (prioritized dependency satisfaction), then verify other dependencies, perserving interface consistency for multi-port interfaces)

                        # compatible_state_list = port.find_compatible_ports(system.components)
                        compatibility = port.find_compatible_states(system.components)
                        compatible_state_list = compatibility[2] # compatible_state_list = port.find_compatible_states(system.components)

			#compatible_state_list = component.find_compatible_components(system.components)
			#compatible_state_list = port.find_compatible_ports(system.components)
			#compatible_state_list = port.find_compatible_states(other_ports)
                        # component.find_compatible_components(component_list_or_system)
                        # port.find_compatible_ports(other_component_or_components)
                        # port.find_compatible_states(other_port)
                        # state.find_compatible_
                        # 
                        # 

                        # Print the compatible states and corresponding ports (if any).
                        # For components that provide no compatible ports, print 'None'.
                        print '\t\tCompatible Ports:'
                        for compatible_state in compatible_state_list:
                            print "\t\t\t%s: mode: %s, direction: %s, voltage: %s" % (compatible_state.port.number, compatible_state.mode, compatible_state.direction, compatible_state.voltage)
                            # print "\t\t\tPort %s:" % compatible_state.number

#---

                        # for component in compatible_port_list:

                                # if len(compatible_port_list[component]) == 0:
                                        # print '\t\t\t%s: None' % component.name
                                # else:
                                        # print '\t\t\t%s:' % component.name

                                # for port in compatible_port_list[component]:
                                        # print '\t\t\t\tPort %s:' % port.number
                                        # for compatible_port in compatible_port_list[component][port]:
                                                # print '\t\t\t\t\t%s, %s, %s' % (compatible_port['state']['mode'], compatible_port['state']['direction'], compatible_port['state']['voltage'])


			# Generate list of compatible paths
			# TODO: Make sure all required information is stored...
			# for compatible_port in compatible_ports:
				# path = api.Path()
				# path.ports.append(port)
				# path.ports.append(compatible_port)

				# paths.append(path)

		print ''

	print 'AVAILABLE PATHS:'
	for path in paths:
		print path

	# TODO: Generate list of valid paths.

	print 'TODO: Generate step-by-step instructions. Update connections on the fly as connections are made? Sure, but add option for automating.'

	print 'TODO: Generate path YAML file.'

def select_compatible_port(port, compatible_port_list):
	"""
	Selects a port from `compatible_port_list` to which `port` will be connected with a path.
	"""
	None

if __name__ == "__main__":
	assemble()
