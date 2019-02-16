#!/usr/bin/env python3

from datetime import datetime


class Machine:
    def __init__(self, machinename, machineinfo, model):
        self.notes = []
        self.units = []
        self.constraints = ""
        self.hardware = {}
        self.hardware["arch"] = ""
        self.hardware["cores"] = ""
        self.hardware["mem"] = ""
        self.hardware["root-disk"] = ""
        self.hardware["availability-zone"] = ""

        self.name = machinename
        self.jujustatus = machineinfo["juju-status"]["current"]
        self.jujusince = datetime.strptime(
            machineinfo["juju-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        self.jujuversion = machineinfo["juju-status"]["version"]
        self.dnsname = machineinfo["dns-name"]
        self.ipaddresses = machineinfo["ip-addresses"]
        self.instanceid = machineinfo["instance-id"]
        self.machinestatus = machineinfo["machine-status"]["current"]
        self.machinemessage = machineinfo["machine-status"]["message"]
        self.machinesince = datetime.strptime(
            machineinfo["machine-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        self.series = machineinfo["series"]
        if "constraints" in machineinfo:
            self.constraints = machineinfo["constraints"]
        for hardwarepair in machineinfo["hardware"].split(" "):
            key, value = hardwarepair.split("=")
            self.hardware[key] = value
