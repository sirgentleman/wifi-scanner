from . import nettools
from . import utils
import os
import csv
import datetime

MAP_FILE_PATH = os.path.join(os.path.expanduser("~"), "mapped_macs.csv")


class NetworkState:
    def __init__(self, net_interface):
        self.net_interface = net_interface
        self.curr_connected = []
        self.device_map = []
        self.field_names = ["name", "mac", "mac_vendor", "last_seen"]

    def save_map(self):
        with open(MAP_FILE_PATH, newline='', mode="w") as mapfile:
            writer = csv.DictWriter(mapfile, fieldnames=self.field_names)
            writer.writeheader()
            for device in self.device_map:
                writer.writerow(device)

    def load_map(self):
        if not os.path.exists(MAP_FILE_PATH):
            return

        with open(MAP_FILE_PATH, newline='', mode="r") as mapfile:
            self.device_map = []
            reader = csv.DictReader(mapfile)
            for row in reader:
                self.device_map.append(row)

    def scan(self):
        arp_devices = nettools.get_connected_devices(
            self.net_interface["address"], self.net_interface["mask"])
        self.curr_connected = []
        for connected in arp_devices:
            found_device = self._find_device(connected)
            if found_device is None:
                new_device = {
                    "name": "UNNAMED",
                    "mac": connected["mac"],
                    "mac_vendor": utils.get_vendor(connected["mac"]),
                    "last_seen": connected["timestamp"]
                }
                self.device_map.append(new_device)
                self.curr_connected.append(new_device)
            else:
                found_device["last_seen"] = connected["timestamp"]
                self.curr_connected.append(found_device)

    def _find_device(self, input_device):
        for device in self.device_map:
            if input_device["mac"] == device["mac"]:
                return device
        return None
