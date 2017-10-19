import yaml

from ..util import util
from port import Port
from state import State
from system import System

class Component(object):

    def __init__(self, component_dict=None):
        """ The ``Component`` class represents a device.

        A component stores state individually for each instance and can be
        configured by passing in parameters using a structure that reprsents
        the state.

        Args:
            path (str): path to a model yaml file.
        """

        self.name = None
        self.ports = []

        # Load name from component data file
        if 'name' in component_dict:
            self.name = component_dict['name']

        # Load host flag from component data file
        if 'host' in component_dict:
            self.host = component_dict['host']
        else:
            self.host = False

        # Load ports from component data file
        for port_dict in component_dict['ports']:
            port = Port(self, port_dict)
            self.ports.append(port)

        # self.compute_port_dependencies()


    def get_ports(self):
        # TODO: return list of ports
        # TODO: device.ports
        return self.ports

    @staticmethod
    def open(paths):
        """
        Reads the model files located at the specified paths and returns a list of
        model objects.
        """
        components = []
        for path in paths:
            if path != None:
                component_dict = util.load_yaml_file(path)
                component = Component(component_dict)
                components.append(component)
        return components

    @staticmethod
    def compose(components):
        """
        Determines whether the components can be connected or not.
        If they can be connected, it searches for valid connections.
        If a complete, valid set of connections is found, the connections are returned.
        (The returned connections are used to describe step by step connections + chart.)
        (The returned connections are written to a file.)

        Parameters
        ----------
        components : list of components
            List of ``Component`` objects to compose into a ``System``.

        Notes
        -----
        # route(components)
        # Pseudocode:
        # Start with devices that have _only_ a single configuration per port.
        # - seek power sources
        # - for a found power source, check if the source also satisfies the other dependencies
        # - if so, find connections on the device
        # - if not, continue to next power source candidate...
        """
        # TODO: search for compatible device (first look for power source (prioritized dependency satisfaction), then verify other dependencies, perserving interface consistency for multi-port interfaces)

        logger = util.logger(__name__, exclude_prefix=True)

        system = System()
        system.components.extend(components)

        # TODO: Infer hosts or ask user interactively or store in YAML file
        hosts = []
        for component in system.components:
            if component.host:
                hosts.append(component)

        paths = []
        occupied_ports = []

        for component in system.components:
            if component in hosts:
                logger.info('Skipping compatibility search for host %s.\n' % component.name)
                continue

            # THE JOB IS THE FILL THIS ARRAY WITH ALL PORTS FOR THE COMPONENT! IF THEY'RE NOT ALL IN THERE AT THE END OF THIS LOOP, IT IS AN INCOMPLETE INTERFACE.
            resolved_source_component_ports = []

            # print 'Searching for compatible ports for %s:' % component.name
            for port in component.ports:
                compatibility = port.find_compatible_states(system.components, logger)

                # Print the compatible states and corresponding ports (if any).
                # For components that provide no compatible ports, print 'None'.
                logger.info('\t\tCompatible Ports:')
                for compatible_state in port.get_compatible_states():
                    logger.info("\t\t\t%s: mode: %s, direction: %s, voltage: %s" % (
                        compatible_state.port.number, compatible_state.mode, compatible_state.direction, compatible_state.voltage))

                    if compatible_state.port not in occupied_ports and port not in resolved_source_component_ports:
                        occupied_ports.append(compatible_state.port)
                        resolved_source_component_ports.append(port)

                        path = {
                            'source_component': port.component,
                            'source_port': port,
                            'target_component': compatible_state.port.component,
                            'target_port': compatible_state.port
                        }

                        paths.append(path)

            logger.info('')

        print "\nGenerated configuration file with paths in <YAML_FILE_LOCATION>."
        print "\nGenerated scripts with configured components in <LOCATIONS>. To customize behavior, edit <FILES>."

        print "\nAssembly Instructions:"
        for path in paths:
            print 'Connect the component: %s:' % path['source_component'].name
            print '\tConnect port %s on %s to port %s on %s' % (path['source_port'].number, path['source_component'].name, path['target_port'].number, path['target_component'].name)

        # TODO: add flag "--explain" to explain why certain ports were chosen (based on heuristic).
        # TODO: Generate list of valid paths.
        # print 'TODO: Generate step-by-step instructions. Update connections on the fly as connections are made? Sure, but add option for automating.'
        # print 'TODO: Generate path YAML file.'

"""
device = Component()
supported_voltages = device.get_ports()[0].get_model().get_voltages()

is_supported_config = device.get_ports()[0].get_model().get_voltages()

----

device.ports.get(number=3)      # Low-level API (for on-device, calls into platform API)
device.ports.get('adc')         # High-level API (for controllers)

----

devices                                # list of available devices
device.ports()                         # list of ports attached to the device
device.ports(3, 4)                     # list of ports attached to the device
device.ports(3, 4).voltage
device.ports(3, 4).get('mode', 'voltage')
device.ports(3, 4).set('mode': 'digital', 'voltage': '5v')

----

device.ports.get('adc').set(adc=844)
    device.ports.get('adc').sample(adc=844)
    single_sample_value = device.ports.get('adc').sample()
        device.ports.get('adc').value(adc=844)
        single_sample_value = device.ports.get('adc').value()
device.ports.get('adc').publish(adc=844)
device.ports.get('adc').publish(voltage=2.4)
device.ports.get('adc').publish(voltage=2.4)
adc_value_stream = device.ports.get('adc').subscribe()

// path_config = assemble(device_001, device_002)

device.ports.get(3).voltage
device.ports.get(3).validate(mode='digital', direction='input', voltage='5v')
device.ports.get(3).configure(mode='digital', direction='input', voltage='5v')

device.ports.get([3,5,8]).validate(mode='digital', voltage='5v')
device.ports.get([3,5,8]).value(mode='digital', voltage='5v')
device.ports.set([3,5,8]).value(mode='digital', voltage='5v')

device.ports(3).voltage
device.ports(3).validate(mode='digital', direction='input', voltage='5v')
device.ports(3).configure(mode='digital', direction='input', voltage='5v')
device.ports([3,4,8]).voltage

device.ports[3].voltage
device.ports[3].validate(mode='digital', direction='input', voltage='5v')
device.ports[3].configure(mode='digital', direction='input', voltage='5v')

??? device.interfaces
system.interfaces                       # .interfaces only for system, not device? device analog is port?
system.interfaces.get('right-motor')    # interface name is specified in path name and yaml interface cfg
system.interfaces.get('robot').controller

Note:
Using the following has a parallel UI in the mobile app (i.e., diff levels of abstraction in zoom levels)
    `device.ports.*`
    `system.interfaces.*`

interfaces = device.get_interfaces()
interfaces['interface-name'].ports
"""
