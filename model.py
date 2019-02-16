#!/usr/bin/env python3

from datetime import datetime


class Model:
    # TODO get latest juju version dynamically
    latest_juju_version = "2.5.1"

    def __init__(self, modelinfo, controller):
        self.notes = []
        self.applications = []
        self.machines = []
        self.meterstatus = ""
        self.message = ""

        self.name = modelinfo["name"]
        self.type = modelinfo["type"]
        self.controller = controller
        self.controller.name = modelinfo["controller"]
        self.cloud = modelinfo["cloud"]
        self.version = modelinfo["version"]
        self.modelstatus = modelinfo["model-status"]["current"]
        self.since = datetime.strptime(
            modelinfo["model-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        if "meter-status" in modelinfo:
            self.meterstatus = modelinfo["meter-status"]["color"]
            self.message = modelinfo["meter-status"]["message"]
        self.sla = modelinfo["sla"]

    def add_application(self, application):
        self.applications.append(application)

    def add_machine(self, machine):
        self.machines.append(machine)

    def get_machine(self, machinename):
        for machine in self.machines:
            if machine.name == machinename:
                return machine
        else:
            return None
