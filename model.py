#!/usr/bin/env python3

import re
from colors import Color
from packaging import version
import pendulum


class Model:
    # TODO get latest juju version dynamically
    latest_juju_version = version.parse("2.5.1")
    column_names = [
        "Model",
        "Controller",
        "Cloud/Region",
        "Version",
        "SLA",
        "Timestamp",
        "Model-Status",
        "Meter-Status",
        "Message",
        "Notes",
    ]

    def __init__(self, modelinfo, controller):
        """
        Create a Model object with basic information from a model object
        from a juju status output
        """
        # Default Values
        self.notes = []
        self.applications = []
        self.machines = []
        self.containers = []
        self.meterstatus = ""
        self.message = ""
        self.upgradeavailable = ""

        # Required Variables
        self.name = modelinfo["name"]
        self.type = modelinfo["type"]
        self.controller = controller
        self.controller.name = modelinfo["controller"]
        self.cloud = modelinfo["cloud"]
        self.version = modelinfo["version"]
        self.modelstatus = modelinfo["model-status"]["current"]
        self.sla = modelinfo["sla"]

        # Required Dates
        if re.match(r".*Z$", modelinfo["model-status"]["since"]):
            self.since = pendulum.from_format(
                modelinfo["model-status"]["since"],
                "DD MMM YYYY HH:mm:ss",
                tz="UTC",
            )
        else:
            self.since = pendulum.from_format(
                modelinfo["model-status"]["since"], "DD MMM YYYY HH:mm:ssZ"
            )
        controller.update_timestamp(self.since)

        # Optional Variables
        if "meter-status" in modelinfo:
            self.meterstatus = modelinfo["meter-status"]["color"]
            self.message = modelinfo["meter-status"]["message"]
        if "upgrade-available" in modelinfo:
            self.upgradeavailable = modelinfo["upgrade-available"]
            self.notes.append("upgrade available: " + self.upgradeavailable)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def add_application(self, application):
        """Add an Application to this model"""
        self.applications.append(application)

    def add_machine(self, machine):
        """Add a machine to this model"""
        self.machines.append(machine)

    def add_container(self, container):
        """Add a container to this model"""
        self.containers.append(container)

    def get_application(self, appname):
        """Get an Application by name"""
        for application in self.applications:
            if application.name == appname:
                return application
        else:
            return None

    def get_machine(self, machinename):
        """Get a machine by name"""
        for machine in self.machines:
            if machine.name == machinename:
                return machine
        else:
            return None

    def get_container(self, containername):
        """Get a container by name"""
        for container in self.containers:
            if container.name == containername:
                return container
        else:
            return None

    def get_version_color(self):
        """Return a version string with correct colors based on version"""
        model_version = version.parse(self.version)
        if (
            model_version < version.parse("2.0.0")
            or model_version > Model.latest_juju_version
        ):
            return Color.Fg.Red + self.version + Color.Reset
        elif model_version < Model.latest_juju_version:
            return Color.Fg.Yellow + self.version + Color.Reset
        else:
            return Color.Fg.Green + self.version + Color.Reset

    # TODO Figure out all possible values of all options and color accordingly
    def get_modelstatus_color(self):
        """Return a status string with correct colors based on status"""
        if self.modelstatus == "available":
            return Color.Fg.Green + self.modelstatus + Color.Reset
        else:
            return Color.Fg.Red + self.modelstatus + Color.Reset

    def get_meterstatus_color(self):
        """
        Return a meter status string with correct colors based on meter
        status
        """
        if not self.meterstatus:
            return ""
        if self.meterstatus == "green":
            return Color.Fg.Green + self.meterstatus + Color.Reset
        elif self.meterstatus == "red":
            return Color.Fg.Red + self.meterstatus + Color.Reset
        elif self.meterstatus == "amber":
            return Color.Fg.Orange + self.meterstatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.meterstatus + Color.Reset

    def get_row(self, color):
        """Return a list which can be used for a row in a table."""
        if not self.controller.timestampprovided:
            if color:
                self.notes.append(
                    Color.Fg.Yellow + "Guessing at timestamp" + Color.Reset
                )
            else:
                self.notes.append("Guessing at timestamp")
        notesstr = ", ".join(self.notes)
        timestampstr = self.controller.timestamp.strftime("%H:%M:%SZ")
        if color:
            return [
                self.name,
                self.controller.name,
                self.cloud,
                self.get_version_color(),
                self.sla,
                timestampstr,
                self.get_modelstatus_color(),
                self.get_meterstatus_color(),
                self.message,
                notesstr,
            ]
        else:
            return [
                self.name,
                self.controller.name,
                self.cloud,
                self.version,
                self.sla,
                timestampstr,
                self.modelstatus,
                self.meterstatus,
                self.message,
                notesstr,
            ]
