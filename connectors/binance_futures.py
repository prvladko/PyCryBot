import logging
import requests
import time
import typing

from urllib.parse import urlencode

import hmac
import hashlib

import websocket
import json

import threading

from models import *

logger = logging.getLogger()

class BinanceFuturesClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool):
        if testnet:
            self.base_url = 'https://testnet.binancefuture.com'
            self.wss_url = 'wss://stream.binancefuture.com/ws'  # in documentation 'wss://testnet.binancefuture.com' wtf???
        else:
            self.base_url = 'https://fapi.binance.com'
            self.wss_url = 'wss://fstream.binance.com/ws'

        self.public_key = public_key
        self.secret_key = secret_key

        self.headers = {'X-MBX-APIKEY': self.public_key}

        self.contracts = self.get_contracts()
        self.balances = self.get_balances()

        self.prices = dict()

        self.ws_id = 1
        self.ws = None

        t = threading.Thread(target=self.start_ws)
        t.start()

        logger.info('Binance Futures Client is successfully initialized')

    def generate_signature(self, data: typing.Dict) -> str:
        return hmac.new(self.secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()  # convert from string to bit code

    def make_request(self, method: str, endpoint: str, data: typing.Dict):  # doesn't return the same output, so can be None o JSON object, not going to type it with '->'
        if method == 'GET':
            try:
                response = requests.get(self.base_url + endpoint, params=data, headers=self.headers)
            except Exception as e:
                logger.error('Connection error while making %s request to %s: %s', method, endpoint, e)
                return None

        elif method == 'POST':
            try:
                response = requests.post(self.base_url + endpoint, params=data, headers=self.headers)
            except Exception as e:
                logger.error('Connection error while making %s request to %s: %s', method, endpoint, e)
                return None

        elif method == 'DELETE':
            try:
                response = requests.delete(self.base_url + endpoint, params=data, headers=self.headers)
            except Exception as e:
                logger.error('Connection error while making %s request to %s: %s', method, endpoint, e)
                return None

        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error('Error while making %s request to %s: %s (error code %s)',
                         method, endpoint, response.json(), response.status_code)
            return None  #

    def get_contracts(self) -> typing.Dict[str, Contract]:  # returns a specified dictionary with str as keys & Contract object as values
        exchange_info = self.make_request('GET', '/fapi/v1/exchangeInfo', dict())

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = Contract(contract_data)
        #contracts['BTCUSDT'].price_decimals  # is just for testing

        return contracts

    def get_historical_candles(self, contract: Contract, interval: str) -> typing.List[Candle]:
        data = dict()
        data['symbol'] = contract.symbol
        data['interval'] = interval
        data['limit'] = 1000

        raw_candles = self.make_request('GET', '/fapi/v1/klines', data)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append(Candle(c))
        #candles[-1].low

        return candles

    def get_bid_ask(self, contract: Contract) -> typing.Dict[str, float]:
        #'https://testnet.binancefuture.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT'  # can add parameters with "&" FOR EXAMPLE ...?symbol=BTCUSDT&key=value&key2=value2'
        data = dict()
        data['symbol'] = contract.symbol
        ob_data = self.make_request('GET', '/fapi/v1/ticker/bookTicker', data)

        if ob_data is not None:
            if contract.symbol not in self.prices:
                self.prices[contract.symbol] = {'bid': float(ob_data['bidPrice']), 'ask': float(ob_data['askPrice'])}
            else:
                self.prices[contract.symbol]['bid'] = float(ob_data['bidPrice'])
                self.prices[contract.symbol]['ask'] = float(ob_data['askPrice'])

            return self.prices[contract.symbol]

    def get_balances(self) -> typing.Dict[str, Balance]:
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        balances = dict()
        account_data = self.make_request('GET', '/fapi/v1/account', data)

        if account_data is not None:
            for a in account_data['assets']:
                balances[a['asset']] = Balance(a)
        #print(balances['USDT'].wallet_balance)

        return balances

    def place_order(self, contract: Contract, side: str, quantity: float, order_type: str, price=None, tif=None)  -> OrderStatus:
        data = dict()
        data['symbol'] = contract.symbol
        data['side'] = side
        data['quantity'] = quantity
        data['type'] = order_type

        if price is not None:
            data['price'] = price

        if tif is not None:
            data['timeInForce'] = tif

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request('POST', '/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)

        return order_status

    def cancel_order(self, contract: Contract, order_id: int)  -> OrderStatus:
        data = dict()
        data['symbol'] = contract.symbol
        data['orderID'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        order_status = self.make_request('DELETE', '/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)

        return order_status

    def get_order_status(self, contract: Contract, order_id: int) -> OrderStatus:

        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['symbol'] = contract.symbol
        data['orderID'] = order_id
        data['signature'] = self.generate_signature(data)
        order_status = self.make_request('GET', '/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)

        return order_status

    def start_ws(self):
        self.ws = websocket.WebSocketApp(self.wss_url, on_open=self.on_open, on_close=self.on_close, on_error=self.on_error, on_message=self.on_message)
        self.ws.run_forever()  # infinite loop

    def on_open(self, ws):
        logger.info('Binance Websocket connection opened')

        self.subscribe_channel('BTCUSDT')

    def on_close(self, ws):
        logger.warning('Binance Websocket connection closed')

    def on_error(self, ws, msg: str):
        logger.error('Binance connection error: %s', msg)

    def on_message(self, ws, msg: str):

        data = json.loads(msg)

        if 'e' in data:
            if data['e'] == 'bookTicker':

                symbol = data['s']

                if symbol not in self.prices:
                    self.prices[symbol] = {'bid': float(data['b']), 'ask': float(data['a'])}
                else:
                    self.prices[symbol]['bid'] = float(data['b'])
                    self.prices[symbol]['ask'] = float(data['a'])

    def subscribe_channel(self, contract: Contract):
        data = dict()
        data['method'] = 'SUBSCRIBE'
        data['params'] = []  # list of channels to subscribe too
        data['params'].append(contract.symbol.lower() + '@bookTicker')
        data['id'] = self.ws_id

        print(data, type(data))
        print(json.dumps(data), type(json.dumps(data)))

        try:
            self.ws.send(json.dumps(data))
        except Exception as e:
            logger.error('Websocket error while subscribing to %s: %s', contract.symbol, e)
            return None

        self.ws_id += 1