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

    def get_contracts(self):
        return

    def get_historical_candles(self):
        return

    def get_bid_ask(self):
        return