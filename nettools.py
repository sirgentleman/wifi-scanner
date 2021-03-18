#! .venv/bin/python3

import subprocess
import nettoolbox as ntb
import re
import concurrent.futures


class NetworkAddr:

    _ip_regex = "^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]){1}(\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])){3}$"

    def __init__(self, ip_addr):
        assert(re.search(self._ip_regex, ip_addr)), "Address should be in decimal format!"
        self.octets =  list(map(int, ip_addr.split('.')))
        self._binary = (self.octets[0] << 24) | (self.octets[1] << 16) | (self.octets[2] << 8) | self.octets[3]

    def increment(self):
        self._binary += 1
        for i in range(4):
            self.octets[3-i] = (self._binary & (255 << i*8)) >> i*8

    def __str__(self):
        result = ""
        for i in range(4):
            result += str(self.octets[i])
            if(i != 3):
                result += '.'
        return result


# mask as string
def get_device_amount(mask):
    
    addr = NetworkAddr(mask)    

    final_amount = ((addr.octets[0] ^ 255) << 12) | ((addr.octets[1] ^ 255) << 8) | ((addr.octets[2] ^ 255) << 4) | (addr.octets[3] ^ 255)

    return final_amount - 1

def get_network_address(machine_ip, mask):

    machine_addr = NetworkAddr(machine_ip)
    mask_addr = NetworkAddr(mask)

    result = ""
    for i in range(4):
        result += str(machine_addr.octets[i] & mask_addr.octets[i])
        if(i != 3):
            result += '.'

    return result

def ping_host(ip_addr, retries):

    command = ['ping', '-q', '-c', str(retries), str(ip_addr)]

    return subprocess.call(command) == 0