from state import State

class System(object):

    def __init__(self):
        self.components = []
        self.paths = []

    def add_component(self, component):
        self.components.append(component)

    def add_path(self, path):
        self.paths.append(path)


    # TODO: locate_compatible_interface(...)
    def find_compatible_ports(self, source_port, include_component_ports=False):
	"""
	Locates a port on the specified model that matches the specfied port_dependency.
	todo: parallelize this function... so many nested loops!

        If the `include_component_ports` is True, then the ports on the source
        component will be included in the search for ports. This enables the
        component to connect its ports to each other.
	"""
	print '\tPort %s on %s:' % (source_port.number, source_port.component.name)
	print '\t\tStates: %s' % source_port.states
	print '\t\tDependencies: %s' % source_port.compatible_state_set

        compatible_ports = []
	for component in self.components:

		# Prevent attempt to search for compatible ports on the same component 
		# TODO: Add option to enable searching on the same component 
                if include_component_ports and component is source_port.component:
                        continue

		# print 'Port Dependencies for %s:' % model.name
		for port in component.ports:

			for state in port.states:

				# Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
				# Search through ALL possible combination pairs for all mode,direction,voltage combos on ports... and store list of possibilities!
				# TODO: expand this state sooner? or use cached computation?
				# port_configuration_list = port.compute_state_set(state)

				# Determine compatible ports
				for compatible_state in source_port.compatible_state_set:

                                        if State.compare(state, compatible_state):

                                                # Just-in-time initialize storage for compatible port states on other component's port to empty list

                                                compatible_ports.append(state)

	return compatible_ports
