class Interface(object):

    def __init__(self, mode=None, direction=None, voltage=None):
        self.mode = mode if mode is not None else None
        self.direction = direction if direction is not None else None
        self.voltage = voltage if voltage is not None else None

        self.source_component = None
        self.source_port = None
        self.source_state = None

        self.target_component = None
        self.target_port = None
        self.target_state = None
