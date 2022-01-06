import typing

import dateutil.parser
import datetime

BITMEX_MULTIPLIER = 0.00000001
BITMEX_TF_MINUTES = {'1m': 1, '5m': 5, '1h': 60, '1d': 1440}

class Balance:
    def __init__(self, balance_info: typing.Dict, exchange: str):
        if exchange == "binance":
            self.initial_margin = float(balance_info['initialMargin'])
            self.maintenance_margin = float(balance_info['maintMargin'])
            self.margin_balance = float(balance_info['marginBalance'])
            self.wallet_balance = float(balance_info['walletBalance'])
            self.unrealized_pnl = float(balance_info['unrealizedProfit'])

        elif exchange == "bitmex":
            self.initial_margin = balance_info['initMargin'] * BITMEX_MULTIPLIER
            self.maintenance_margin = balance_info['maintMargin'] * BITMEX_MULTIPLIER
            self.margin_balance = balance_info['marginBalance'] * BITMEX_MULTIPLIER
            self.wallet_balance = balance_info['walletBalance'] * BITMEX_MULTIPLIER
            self.unrealized_pnl = balance_info['unrealisedPnl'] * BITMEX_MULTIPLIER

class Candle:
    def __init__(self, candle_info: typing.Dict, timeframe, exchange: str):
        if exchange == "binance":
            self.timestamp = candle_info[0]
            self.open = float(candle_info[1])
            self.high = float(candle_info[2])
            self.low = float(candle_info[3])
            self.close = float(candle_info[4])
            self.volume =  float(candle_info[5])

        elif exchange == "bitmex":  # https://www.bitmex.com/api/explorer/#!/Trade/Trade_getBucketed
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

        elif exchange == "parse_trade":
            self.timestamp = candle_info['ts']
            self.open = candle_info['open']
            self.high = candle_info['high']
            self.low = candle_info['low']
            self.close = candle_info['close']
            self.volume = candle_info['volume']


def tick_to_decimals(tick_size: float) -> int:
    tick_size_str = '{0:.8f}'.format(tick_size)
    while tick_size_str[-1] == '0':
        tick_size_str = tick_size_str[:-1]

    split_tick = tick_size_str.split('.')

    if len(split_tick) > 1:  # example '0.001'
        return len(split_tick[1])
    else:
        return 0


class Contract:
    def __init__(self, contract_info: typing.Dict, exchange: str):
        if exchange == 'binance':
            # print(contract_info)  # just for test in 028 chapter
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
            self.price_decimals = tick_to_decimals(contract_info['tickSize'])
            self.quantity_decimals = tick_to_decimals(contract_info['lotSize'])
            self.tick_size = contract_info['tickSize'] # 0.01
            self.lot_size = contract_info['lotSize']

            self.quanto = contract_info['isQuanto']
            self.inverse = contract_info['isInverse']

            self.multiplier = contract_info['multiplier'] * BITMEX_MULTIPLIER  # from Satoshi to Bitcoin

            if self.inverse:
                self.multiplier *= -1


class OrderStatus:
    def __init__(self, order_info: typing.Dict, exchange: str):
            if exchange == 'binance':
                self.order_id = order_info['orderId']
                self.status = order_info['status'].lower()
                self.avg_price = float(order_info['avgPrice'])
            elif exchange == 'bitmex':
                self.order_id = order_info['orderID']
                self.status = order_info['ordStatus'].lower()
                self.avg_price = float(order_info['avgPx'])


class Trade:
    def __init__(self, trade_info):
        self.time: int = trade_info['time']
        self.contract: int = trade_info['contract']
        self.strategy: int = trade_info['strategy']
        self.side: int = trade_info['side']
        self.entry_price: int = trade_info['entry_price']
        self.status: int = trade_info['status']
        self.pnl: int = trade_info['pnl']
        self.quantity: int = trade_info['quantity']
        self.entry_id: int = trade_info['entry_id']