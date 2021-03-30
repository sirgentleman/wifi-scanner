import nettools
import csv

class NetworkState:

    def __init__(self, net_interface):
        self.curr_connected = nettools.get_connected_devices(net_interface["address"], net_interface["mask"])
        self.device_map = [{"name" : "NAME", "mac" : "address"}]


    def save_map(self):
        with open("mapped_macs.csv", newline='', mode="w") as mapfile:
            field_names = ["name", "mac"]
            writer = csv.DictWriter(mapfile, fieldnames=field_names)
            writer.writeheader()
            for device in self.device_map:
                writer.writerow(device)

    def load_map(self):
        with open("mapped_macs.csv", newline='', mode="r") as mapfile:
            self.device_map = []
            field_names = ["name", "mac"]
            reader = csv.DictReader(mapfile)
            for row in reader:
                self.device_map.append(row)
