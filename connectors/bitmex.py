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
# 017 Bitmex - REST API & Authentication---
class BitmexClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool):

        if testnet:
            self._base_url = 'https://testnet.bitmex.com'
            self._wss_url = 'wss://testnet.bitmex.com/realtime'
        else:
            self._base_url = 'https://www.bitmex.com'
            self._wss_url = 'wss://www.bitmex.com/realtime'

        self._public_key = public_key
        self._secret_key = secret_key

        self._ws = None

        self.contracts = self.get_contracts()
        self.balances = self.get_balances()

        self.prices = dict()

        t = threading.Thread(target=self._start_ws)
        t.start()

        logger.info('Bitmex Client successfully initialized')