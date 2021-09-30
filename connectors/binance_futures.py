import logging
import requests

logger = logging.getLogger()

class BinanceFuturesClient:
    def __init__(self, testnet):
        if testnet:
            self.base_url = 'https://testnet.binancefuture.com'
        else:
            self.base_url = 'https://fapi.binance.com'

        logger.info('Binance Futures Client is successfully initialized')

    def make_request(self, method, endpoint, data):
        if method == 'GET':
            response = requests.get(self.base_url + endpoint, params=data)
        else:
            raise ValueError()

        if response.status_code == '200':
            return response.json()
        else:
            logger.error('Error while making %s request to %s: %s (error code %s)',
                         method, endpoint, response.json(), response.status_code)
            return None

    def get_contracts(self):
        exchange_info = self.make_request('GET', 'fapi/v1/exchangeInfo', None)

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = contract_data
        return contracts

    def get_historical_candles(self):
        requests.get()
        return

    def get_bid_ask(self):
        requests.get()
        return