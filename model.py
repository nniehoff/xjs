class Model:
    latest_juju_version = '2.5.1'

    def __init__(self, modelinfo):
        self.name = modelinfo['name']
        self.type = modelinfo['type']
        # TODO: This should be a pointer at a controller object
        self.controller = modelinfo['controller']
        self.cloud = modelinfo['cloud']
        self.version = modelinfo['version']
