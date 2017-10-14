class State(object):

    def __init__(self, port=None, state_dict=None):
        self.port = port

        self.mode = state_dict['mode'] if state_dict is not None else None
        self.direction = state_dict['direction'] if state_dict is not None else None
        self.voltage = state_dict['voltage'] if state_dict is not None else None

        self.__compatible_states = []

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
    def compute_states(port, states_dict):
        """
        Expands the state expression into discrete states and returns an array
        containing the discrete states.
        """
        # Compute complete list of the available configurations of the port (FOR A PARTICULAR STATE STATE)
        # Search through ALL possible combination pairs for all
        # mode,direction,voltage combos on ports... and store list of
        # possibilities!

        port_states = []
        for mode in states_dict['mode']:
            for direction in states_dict['direction']:
                for voltage in states_dict['voltage']:
                    state = State(port, {'mode': mode, 'direction': direction, 'voltage': voltage})
                    # state = State(port, mode, direction, voltage)
                    port_states.append(state)
        return port_states 

    def get_compatible_states(self):
        return self.__compatible_states

