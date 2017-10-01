class Project(object):

    def __init__(self):
        self.components = []
        self.paths = []

    def add_component(self, component):
        self.components.append(component)

    def add_path(self, path):
        self.paths.append(path)
