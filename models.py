import typing

import dateutil.parser
import datetime

BITMEX_MULTIPLIER = 0.00000001
BITMEX_TF_MINUTES = {'1m': 1, '5m': 5, '1h': 60, '1d': 1440}

class Balance:
    def __init__(self, balance_info: typing.Dict, exchange: str):
        if exchange == 'binance':
            self.initial_margin = float(balance_info['initialMargin'])
            self.maintenance_margin = float(balance_info['maintMargin'])
            self.margin_balance = float(balance_info['marginBalance'])
            self.wallet_balance = float(balance_info['walletBalance'])
            self.unrealized_pnl = float(balance_info['unrealizedProfit'])

        elif exchange == 'bitmex':
            self.initial_margin = balance_info['initMargin'] * BITMEX_MULTIPLIER
            self.maintenance_margin = balance_info['maintMargin'] * BITMEX_MULTIPLIER
            self.margin_balance = balance_info['marginBalance'] * BITMEX_MULTIPLIER
            self.wallet_balance = balance_info['walletBalance'] * BITMEX_MULTIPLIER
            self.unrealized_pnl = balance_info['unrealisedPnl'] * BITMEX_MULTIPLIER

class Candle:
    def __init__(self, candle_info: typing.Dict, timeframe, exchange: str):
        if exchange == 'binance':
            self.timestamp = candle_info[0]
            self.open = float(candle_info[1])
            self.high = float(candle_info[2])
            self.low = float(candle_info[3])
            self.close = float(candle_info[4])
            self.volume =  float(candle_info[5])

        elif exchange == 'bitmex':  # https://www.bitmex.com/api/explorer/#!/Trade/Trade_getBucketed
            self.timestamp = dateutil.parser.isoparse(candle_info['timestamp'])
            self.timestamp = self.timestamp - datetime.timedelta(minutes=BITMEX_TF_MINUTES[timeframe])
            print(self.timestamp)
            self.timestamp = int(self.timestamp.timestamp() * 1000)
            # print(candle_info['timestamp'], dateutil.parser.isoparse(candle_info['timestamp']), self.timestamp)
            self.open = candle_info['open']
            self.high = candle_info['high']
            self.low = candle_info['low']
            self.close = candle_info['close']
            self.volume = candle_info['volume']

class Contract:
    def __init__(self, contract_info: typing.Dict, exchange: str):
        if exchange == 'binance':
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['baseAsset']
            self.quote_asset = contract_info['quoteAsset']
            self.price_decimals = contract_info['pricePrecision'] #2
            self.quantity_decimals = contract_info['quantityPrecision']
            self.tick_size = 1 / pow(10, contract_info['pricePrecision'])
            self.lot_size = 1 / pow(10, contract_info['quantityPrecision'])

        elif exchange == 'bitmex':  # https://www.bitmex.com/api/explorer/#!/Instrument/Instrument_getActive
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['rootSymbol']
            self.quote_asset = contract_info['quoteCurrency']
            self.tick_size = contract_info['tickSize'] # 0.01
            self.lot_size = contract_info['lotSize']

class OrderStatus:
    def __init__(self, order_info: typing.Dict, exchange: str):
            if exchange == 'binance':
                self.order_id = order_info['orderId']
                self.status = order_info['status']
                self.avg_price = float(order_info['avgPrice'])

            elif exchange == 'bitmex':
                self.order_id = order_info['orderID']
                self.status = order_info['ordStatus']
                self.avg_price = float(order_info['avgPx'])