from state import State

class Port(object):

    # TODO: connected_port(s)

    def __init__(self, number, mode=None, direction=None, voltage=None):
        self.component = None

        self.number = number

        self.mode = mode if mode is not None else None
        self.direction = direction if direction is not None else None
        self.voltage = voltage if voltage is not None else None

        self.states = []

        # state
        self.connected_port = []

        self.compatible_state_set = []

    def configure(self, mode=None, direction=None, voltage=None):
        """ Sets the state of the `Port` if it is valid.
        """
        self.mode = mode or self.mode
        self.direction = direction or self.direction
        self.voltage = voltage or self.voltage
        None

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

        print '\t%s' % self.compatible_state_set
