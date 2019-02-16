#!/usr/bin/env python3

from datetime import datetime


class Controller:
    zerodate = datetime.strptime("00:00:00Z", "%H:%M:%SZ")

    def __init__(self, controllerinfo={}):
        self.notes = []
        self.models = []
        self.timestampprovided = False
        self.timestamp = Controller.zerodate

        if "timestamp" in controllerinfo:
            self.timestampprovided = True
            self.timestamp = datetime.strptime(
                controllerinfo["timestamp"], "%H:%M:%SZ"
            )

    def update_timestamp(self, date):
        # TODO if the timestamp was from the controller info, only look at
        # dates
        print("Not implemented")

    def add_model(self, model):
        self.models.append(model)
