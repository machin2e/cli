class State(object):

    def __init__(self, port=None, mode=None, direction=None, voltage=None):
        self.port = port

        self.mode = mode
        self.direction = direction
        self.voltage = voltage

    # def __eq__(self, other):
        # if isinstance(other, self.__class__):
            # return self.__dict__ == other.__dict__
        # else:
            # return False

    @staticmethod
    def compare(state, other):
        if state.mode == other.mode and state.direction == other.direction and state.voltage == other.voltage:
            return True
        else:
            return False

    @staticmethod
    def compute_state_set(port, state_combination):
        """
        Expands the state expression into discrete states and returns an array
        containing the discrete states.
        """
        # Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
        # Search through ALL possible combination pairs for all
        # mode,direction,voltage combos on ports... and store list of
        # possibilities!

        port_configuration_list = []
        for mode in state_combination['mode']:
            for direction in state_combination['direction']:
                for voltage in state_combination['voltage']:
                    # port_configuration_list.append({'mode': mode, 'direction': direction, 'voltage': voltage})
                    state = State(port, mode, direction, voltage)
                    port_configuration_list.append(state)
        return port_configuration_list
