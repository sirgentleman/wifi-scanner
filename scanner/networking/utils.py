#! .venv/bin/python3

import requests

_MAC_VENDOR_LOOKUP_URL = "https://macvendors.co/api/vendorname/"


def get_vendor(mac_addr):
    #TODO: check input format

    response = requests.post(_MAC_VENDOR_LOOKUP_URL + str(mac_addr))
    return response.text
