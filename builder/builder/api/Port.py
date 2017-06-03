class Port(object):

    def __init__(self, mode=None, direction=None, voltage=None):
        self.mode = mode if mode is not None else None
        self.direction = direction if direction is not None else None
        self.voltage = voltage if voltage is not None else None
