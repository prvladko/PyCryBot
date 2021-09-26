import logging
import requests
import pprint

logger = logging.getLogger()

def get_contracts():
    # response_object = requests.get('https://testnet.binancefuture.com/fapi/v1/exchangeInfo)  # for test
    response_object = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo')  # from https://binance-docs.github.io/apidocs/futures/en/#check-server-time
    print(response_object.status_code)

    for contract in response_object.json()['symbols']:
        print(contract['pair'])

get_contracts()