#!/usr/bin/env python3

from basicmachine import BasicMachine
from container import Container


class Machine(BasicMachine):
    iscontainer = False

    def __init__(self, machinename, machineinfo, model):
        """
        Create a Machine object with basic information from a machine object
        from a juju status output
        """
        # Setup the BasicMachine
        BasicMachine.__init__(self, machinename, machineinfo, model.controller)

        # Default Values
        self.containers = []
        self.constraints = ""
        self.hardware = {}
        self.hardware["arch"] = ""
        self.hardware["cores"] = ""
        self.hardware["mem"] = ""
        self.hardware["root-disk"] = ""
        self.hardware["availability-zone"] = ""

        # Required Variables
        self.model = model

        # Optional Variables
        if "constraints" in machineinfo:
            self.constraints = machineinfo["constraints"]

        # Calculated Values
        for hardwarepair in machineinfo["hardware"].split(" "):
            key, value = hardwarepair.split("=")
            self.hardware[key] = value

        # Handle Containers if any
        if "containers" in machineinfo:
            for containername, containerinfo in machineinfo[
                "containers"
            ].items():
                container = Container(containername, containerinfo, self)
                model.add_container(container)
                self.containers.append(container)

    # TODO: Shouldn't handle color logic at this level
    def get_row(self, color):
        """Return a list which can be used for a row in a table."""
        notesstr = ", ".join(self.notes)

        if color:
            return [
                self.name,
                self.get_jujustatus_color(),
                self.get_machinestatus_color(),
                self.dnsname,
                self.instanceid,
                self.series,
                self.hardware["availability-zone"],
                self.hardware["arch"],
                self.hardware["cores"],
                self.hardware["mem"],
                self.machinemessage,
                notesstr,
            ]
        else:
            return [
                self.name,
                self.jujustatus,
                self.machinestatus,
                self.dnsname,
                self.instanceid,
                self.series,
                self.hardware["availability-zone"],
                self.hardware["arch"],
                self.hardware["cores"],
                self.hardware["mem"],
                self.machinemessage,
                notesstr,
            ]
