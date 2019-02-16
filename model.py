#!/usr/bin/env python3


class Model:
    # TODO get latest juju version dynamically
    latest_juju_version = "2.5.1"

    def __init__(self, modelinfo, controller):
        self.name = modelinfo["name"]
        self.type = modelinfo["type"]
        self.controller = controller
        self.controller.name = modelinfo["controller"]
        self.cloud = modelinfo["cloud"]
        self.version = modelinfo["version"]
        self.modelstatus = modelinfo["model-status"]["current"]
        self.since = modelinfo["model-status"]["since"]
        if 'meter-status' in modelinfo:
            self.meterstatus = modelinfo["meter-status"]["color"]
            self.message = modelinfo["meter-status"]["message"]
        else:
            self.meterstatus = ""
            self.message = ""
        self.sla = modelinfo["sla"]
