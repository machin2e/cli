from port import Port

class Device(object):

    def __init__(self):
        self.ports = []
        self.ports.append(Port(mode='power', direction='input', voltage='3.3v'))
        self.ports.append(Port(mode='power', direction='bidirectional', voltage='0v'))
        self.ports.append(Port(mode='adc', direction='output', voltage='3.3v'))

    def get_ports(self):
        # TODO: return list of ports
        # TODO: device.ports
        return self.ports

def get_model():
    None

def get_state():
    None

def set_state():
    None
