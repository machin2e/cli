class Path(object):

    def __init__(self):
        self.ports = []

    # def configure(self, mode=None, direction=None, voltage=None):
        # """ Sets the state of the `Port` if it is valid.
        # """
        # None

    # - paths:
        # - source: # This is a port
            # device: raspbery-pi-3 # NOTE: This is the model file name
            # number: 6
            # mode: power
            # direction: input
            # voltage: 3.3v
          # target: # This is a port
            # device: servo-1
            # number: 1
            # mode: power
            # direction: output 
            # voltage: 3.3v
        # - source: # This is a port
            # device: raspbery-pi-3 # NOTE: This is the model file name
            # number: 7
            # mode: power(ground)
            # direction: bidirectional
            # voltage: 0v
          # target: # This is a port
            # device: servo-1 # name is generated IF THERE are multiple device instances passed as args
            # number: 2
            # mode: power(ground)
            # direction: bidirectional
            # voltage: 0v
        # - source: # This is a port
            # device: raspbery-pi-3 # NOTE: This is the model file name
            # number: 8
            # mode: pulse-width-modulation
            # direction: output
            # voltage: 3.3v
          # target: # This is a port
            # device: servo-1 # name is generated IF THERE are multiple device instances passed as args
            # number: 3
            # mode: pulse-width-modulation
            # direction: input
            # voltage: 3.3v
