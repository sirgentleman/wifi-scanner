#! .venv/bin/python3

import nettoolbox as ntb
import re

mask_regex = "^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]){1}(\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])){3}$"

# mask as string
def get_device_amount(mask):
    
    assert(re.search(mask_regex, mask)), "Mask should be in decimal format!"
        

    octets = mask.split('.')

    parts = list(map(int, octets))
    final_amount = ((parts[0] ^ 255) << 12) | ((parts[1] ^ 255) << 8) | ((parts[2] ^ 255) << 4) | (parts[3] ^ 255)

    return final_amount - 1

def get_network_address(machine_ip, mask):

    machine_ip_octets = list(map(int, machine_ip.split('.')))
    mask_octets = list(map(int, mask.split('.')))

    result = ""
    for i in range(4):
        result += str(machine_ip_octets[i] & mask_octets[i])
        if(i != 3):
            result += '.'

    return result


