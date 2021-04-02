#! .venv/bin/python3

import subprocess
import nettoolbox as ntb
from . import utils
import re
import concurrent.futures
import itertools
import os
from datetime import datetime


class NetworkAddr:

    _ip_regex = "^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]){1}(\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])){3}$"

    def __init__(self, ip_addr):
        assert (re.search(self._ip_regex,
                          ip_addr)), "Address should be in decimal format!"
        self.octets = list(map(int, ip_addr.split('.')))
        self._binary = (self.octets[0] << 24) | (self.octets[1] << 16) | (
            self.octets[2] << 8) | self.octets[3]

    def increment(self):
        self._binary += 1
        for i in range(4):
            self.octets[3 - i] = (self._binary & (255 << i * 8)) >> i * 8

        return str(self)

    def __str__(self):
        result = ""
        for i in range(4):
            result += str(self.octets[i])
            if (i != 3):
                result += '.'
        return result


# mask as string
def get_device_amount(mask):

    addr = NetworkAddr(mask)

    final_amount = ((addr.octets[0] ^ 255) << 12) | (
        (addr.octets[1] ^ 255) << 8) | (
            (addr.octets[2] ^ 255) << 4) | (addr.octets[3] ^ 255)

    return final_amount - 1


def get_network_address(machine_ip, mask="255.255.255.0"):

    machine_addr = NetworkAddr(machine_ip)
    mask_addr = NetworkAddr(mask)

    result = ""
    for i in range(4):
        result += str(machine_addr.octets[i] & mask_addr.octets[i])
        if (i != 3):
            result += '.'

    return result


def ping_host(ip_addr, retries=1):
    command = ['ping', '-q', '-c', str(retries), str(ip_addr)]
    result = None

    with open(os.devnull, "w") as f:
        result = subprocess.call(command, stdout=f)

    return result == 0


def ping_network(network_ip, network_mask="255.255.255.0"):
    device_amount = get_device_amount(network_mask)
    network_addr = NetworkAddr(network_ip)

    args = ((network_addr.increment(), 3) for _ in range(device_amount))
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=device_amount) as executor:
        executor.map(lambda p: ping_host(*p), args)


def retrieve_devices_info():

    pipe = subprocess.Popen(["arp", "-n"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = pipe.communicate()

    arp_entries = []
    for entry in out.decode().split('\n'):
        entry_arr = entry.split()
        if len(entry_arr) == 5:
            if entry_arr[2] in map(lambda x: x[2], arp_entries):
                continue
            arp_entries.append(entry_arr)

    arp_entries.pop(0)
    return arp_entries


def get_connected_devices(machine_ip, mask="255.255.255.0"):

    ping_network(get_network_address(machine_ip, mask), mask)

    return_devices = []

    for entry in retrieve_devices_info():
        return_devices.append({
            "ip": entry[0],
            "mac": entry[2],
            "mac_vendor": utils.get_vendor(entry[2]),
            "timestamp": datetime.now().ctime()
        })

    return return_devices


def get_interfaces():
    return ntb.get_interfaces()