import logging
import requests
import pprint

logger = logging.getLogger()

def get_contracts():
    # response_object = requests.get('https://testnet.bitmex.com/api/v1/instrument')  # for test
    response_object = requests.get('https://testnet.bitmex.com/api/v1/instrument')  # from https://binance-docs.github.io/apidocs/futures/en/#check-server-time

    contracts = []

    for contract in response_object.json()['symbols']:
        contracts.append(contract['pair'])

    return contracts

print(get_contracts())