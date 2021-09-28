import logging
import requests
import pprint

logger = logging.getLogger()

def get_contracts():
    contracts = []

    response_object = requests.get('https://bitmex.com/api/v1/instrument/active')

    for contract in response_object.json():
        contracts.append(contract['symbol'])

    return contracts

print(get_contracts())