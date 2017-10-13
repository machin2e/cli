from state import State

class Port(object):

    # TODO: connected_port(s)

    def __init__(self, component, number):

        self.component = component

        self.number = number

        self.state = None # This must be one of the states in the port's list of states
        self.states = []

        # state
        self.compatible_state_set = []

    def get_device(self):
        return None

    def get_compatible_ports(self, device_or_port):
        return ["list", "of", "ports"]

    # @staticmethod
    # def compute_state_set(state):
        # # Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
        # # Search through ALL possible combination pairs for all
        # # mode,direction,voltage combos on ports... and store list of
        # # possibilities!
        # port_configuration_list = []
        # for mode in state['mode']:
            # for direction in state['direction']:
                # for voltage in state['voltage']:
                    # port_configuration_list.append({'mode': mode, 'direction': direction, 'voltage': voltage})
        # return port_configuration_list

    def compute_compatible_state_set(self):
        """
        Uses the port's computed state set (expanded from the configuration)
        to compute the corresponding, or compatible, states. One or more of
        these compatible states must be present in another port for that port
        to be compatible with this port. Such a port is refered to as a
        compatible port.

        This is used in the interactive self-assembly procedure for generating
        port connections.
        """

        # TODO: Store these general/unassigned/port-less in a global area so they can be shared. Only the compatible ports will be stored per actual port.

        for state in self.states:

            # TODO: actually look through the state of other components rather than do this abstract indirect way of searching...
            compatible_state = State()

            # Determine mode compatibility
            # TODO: iterate through all available elements of array (for devices like Pi that have multiple states/configs per port)
            # TODO: change 'mode' to 'role' OR 'function', 'service',
            # 'purpose'?
            if 'power' == state.mode:
                compatible_state.mode = 'power'
            elif 'digital' == state.mode:
                compatible_state.mode = 'digital'
            elif 'analog' == state.mode:  # adc?
                compatible_state.mode = 'analog'
            elif 'resistive-touch' == state.mode:
                compatible_state.mode = 'resistive-touch'
            elif 'pulse-width-modulation' == state.mode:
                # alt: PWM, pwm
                compatible_state.mode = 'pulse-width-modulation'
            elif 'i2c(scl)' == state.mode:  # alt: I2C(SCL)
                compatible_state.mode = 'i2c(scl)'
            elif 'i2c(sda)' == state.mode:  # alt: I2C(SDA)
                compatible_state.mode = 'i2c(sda)'
            elif 'spi(sclk)' == state.mode:
                compatible_state.mode = 'spi(sclk)'
            elif 'spi(mosi)' == state.mode:
                compatible_state.mode = 'spi(mosi)'
            elif 'spi(miso)' == state.mode:
                compatible_state.mode = 'spi(miso)'
            elif 'spi(ss)' == state.mode:
                compatible_state.mode = 'spi(ss)'
            elif 'uart(tx)' == state.mode:
                compatible_state.mode = 'uart(rx)'
            elif 'uart(rx)' == state.mode:
                compatible_state.mode = 'uart(tx)'

            # Determine direction compatibility
            # TODO: Double-check this logic... it's not complete!
            if 'input' == state.direction:
                compatible_state.direction = 'output'
            elif 'output' == state.direction:
                compatible_state.direction = 'input'
            elif 'bidirectional' == state.direction:
                compatible_state.direction = 'bidirectional'

            # Determine power compatibility
            # TODO: Support voltage ranges! e.g., [3.3v, 5v]
            if '3.3v' == state.voltage:
                compatible_state.voltage = '3.3v'
            elif '5v' == state.voltage:
                compatible_state.voltage = '5v'
            elif '0v' == state.voltage:
                compatible_state.voltage = '0v'

            # TODO: verify validity before adding to
            # dependency/compatibility list

            # TODO: if not self.contains_state(cs):
            # if compatible_state not in self.compatible_state_set:
                # self.compatible_state_set.append(compatible_state)
            self.compatible_state_set.append(compatible_state)

        # print '\t%s' % self.compatible_state_set

    # TODO: locate_compatible_interface(...)
    def find_compatible_ports(self, components, include_component_ports=False):
	"""
	Locates a port on the specified model that matches the specfied port_dependency.
	todo: parallelize this function... so many nested loops!

        If the `include_component_ports` is True, then the ports on the source
        component will be included in the search for ports. This enables the
        component to connect its ports to each other.
	"""

	print '\tPort %s on %s:' % (self.number, self.component.name)
	print '\t\tStates: %s' % self.states
	print '\t\tDependencies: %s' % self.compatible_state_set

        compatible_ports = []
	for component in components:

		# Prevent attempt to search for compatible ports on the same component 
		# TODO: Add option to enable searching on the same component 
                if include_component_ports and component is self.component:
                        continue

		# print 'Port Dependencies for %s:' % model.name
		for port in component.ports:

			for state in port.states:

				# Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
				# Search through ALL possible combination pairs for all mode,direction,voltage combos on ports... and store list of possibilities!
				# TODO: expand this state sooner? or use cached computation?
				# port_configuration_list = port.compute_state_set(state)

				# Determine compatible ports
				for compatible_state in self.compatible_state_set:

                                        if State.compare(state, compatible_state):

                                                # Just-in-time initialize storage for compatible port states on other component's port to empty list

                                                compatible_ports.append(port)

	return compatible_ports

    # TODO: locate_compatible_interface(...)
    def find_compatible_states(self, components, include_component_ports=False):
	"""
	Locates a port on the specified model that matches the specfied port_dependency.
	todo: parallelize this function... so many nested loops!

        If the `include_component_ports` is True, then the ports on the source
        component will be included in the search for ports. This enables the
        component to connect its ports to each other.
	"""

	print '\tPort %s on %s:' % (self.number, self.component.name)

	print '\t\tStates:'
        for state in self.states:
            print "\t\t\t(%s, %s, %s)" % (state.mode, state.direction, state.voltage)

	print '\t\tDependencies:'
        for state in self.compatible_state_set:
            print "\t\t\t(%s, %s, %s)" % (state.mode, state.direction, state.voltage)

        compatible_components = []
        compatible_ports = []
        compatible_states = []

	for component in components:

		# Prevent attempt to search for compatible ports on the same component 
		# TODO: Add option to enable searching on the same component 
                if include_component_ports and component is self.component:
                        continue

		# print 'Port Dependencies for %s:' % model.name
		for port in component.ports:

			for state in port.states:

				# Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
				# Search through ALL possible combination pairs for all mode,direction,voltage combos on ports... and store list of possibilities!
				# TODO: expand this state sooner? or use cached computation?
				# port_configuration_list = port.compute_state_set(state)

				# Determine compatible ports
				for compatible_state in self.compatible_state_set:

                                        if State.compare(state, compatible_state):

                                                # Just-in-time initialize storage for compatible port states on other component's port to empty list

                                                if component not in compatible_components:
                                                    compatible_components.append(component)

                                                if port not in compatible_ports:
                                                    compatible_ports.append(port)

                                                if state not in compatible_states:
                                                    compatible_states.append(state)

	# return compatible_states
	return (compatible_components, compatible_ports, compatible_states)
