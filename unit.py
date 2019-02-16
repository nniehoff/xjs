#!/usr/bin/env python3

from datetime import datetime


class Unit:
    def __init__(self, unitname, unitinfo, application):
        self.notes = []
        self.openports = []
        self.message = ""
        self.name = unitname

        self.application = application
        self.workloadstatus = unitinfo["workload-status"]["current"]
        if "message" in unitinfo["workload-status"]:
            self.message = unitinfo["workload-status"]["message"]
        self.workloadsince = datetime.strptime(
            unitinfo["workload-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        self.jujustatus = unitinfo["juju-status"]["current"]
        self.jujuversion = unitinfo["juju-status"]["version"]
        self.jujusince = datetime.strptime(
            unitinfo["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        self.machine = application.model.get_machine(unitinfo["machine"])
        if "open-ports" in unitinfo:
            self.openports = unitinfo["open-ports"]
        self.publicaddress = unitinfo["public-address"]
