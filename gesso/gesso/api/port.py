class Port(object):

    # TODO: connected_port(s)

    def __init__(self, number, mode=None, direction=None, voltage=None):
        self.number = number

        self.mode = mode if mode is not None else None
        self.direction = direction if direction is not None else None
        self.voltage = voltage if voltage is not None else None

        self.states = []

        # state
        self.connected_port = []

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

    # def get_interfaces?:
        # None

    # def add_to_interface?:
        # None
