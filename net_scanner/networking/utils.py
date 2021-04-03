#! .venv/bin/python3

import requests
from time import sleep

_MAC_VENDOR_LOOKUP_URL = "https://api.macvendors.com/"


def get_vendor(mac_addr):
    #TODO: check input format

    response = requests.get(_MAC_VENDOR_LOOKUP_URL + str(mac_addr))
    sleep(1) # API requirement
    return response.text
