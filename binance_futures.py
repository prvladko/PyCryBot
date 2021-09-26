import logging
import requests

logger = logging.getLogger()

def get_contracts():
    # for test 'https://testnet.binancefuture.com'
    response_object = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo')  # from https://binance-docs.github.io/apidocs/futures/en/#check-server-time
    print(response_object.status_code, response_object.json())

get_contracts()