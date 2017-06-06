import yaml

from ..util import util

from port import Port

class Device(object):

    def __init__(self, model_uri=None):
        """ The ``Device`` class represents a device.

        Args:
            model_uri (str): path to a model yaml file.
        """
        self.ports = []

        print model_uri
        if model_uri != None:
            model = util.load_yaml_file(model_uri)

            for port_model in model['ports']:
                #print port_model['number']

                port = Port()

                if 'states' in port_model:
                    for state in port_model['states']:
                        port.states.append(state) 
                        #print state['mode']
                        #print state['direction']
                        #print state['voltage']

                self.ports.append(port)

                # Registry URI example:
                # builder.network/mokogobo/builder-8.0.0


    # def get_state(self):

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

"""
device = Device()
supported_voltages = device.get_ports()[0].get_model().get_voltages()

is_supported_config = device.get_ports()[0].get_model().get_voltages()


interfaces = device.get_interfaces()
interfaces['interface-name'].ports
"""
