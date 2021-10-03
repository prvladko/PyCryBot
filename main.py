import tkinter as tk
import logging

from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient

logger = logging.getLogger()

logger.setLevel(
    logging.INFO)  # min logger level (for the 'Debug' level of message to show in info.log change to logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()  # to show up messages in Python terminal
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s  :: %(message)s')  # message what we want is to show (%current time of the log, %logging level,
stream_handler.setFormatter(formatter)  # add formatter to the stream_handler
stream_handler.setLevel(logging.INFO)  # log level of stream_handler

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)  # add stream_handler to the logger instance
logger.addHandler(file_handler)

if __name__ == '__main__':  # statement will be executed only if the main module will be executed

    binance = BinanceFuturesClient('c6e7aca13a233c0175ef4ed481646d2caa897fe21eaa45cfb23a165bee6fc5e6',
                                   '1087241583949a8aa9ba274a310c37783b276c1e84acdcf7de9dae76a83dfa67', True)
    # print(binance.get_balances())  # test modules
    # print(binance.place_order('BTCUSDT', 'BUY', 0.01, 'LIMIT', 20000, 'GTC'))
    # print(binance.get_order_status('BTCUSDT', 2828701453))
    # print(binance.cancel_order('BTCUSDT', 2828701453))

    # candles = binance.get_historical_candles()
    # candles[-1].low

    bitmex = BitmexClient('llCC7kI5cx2O8POBuKHQ_Sae', 'zezzQqyHUNw8wLNZym1VEsGZ4fbundC7rcCRBDp18BSXRfyJ', True)

    # print(bitmex.contracts['XBTUSD'].base_asset, bitmex.contracts['XBTUSD'].price_decimals)
    # print(bitmex.balances['XBt'].wallet_balance)  # Bitmex returns XBt (symbol of 'satoshi) instead of XBT (symbol of Bitcoin)

    print(bitmex.place_order(bitmex.contracts['XBTUSD'], 'Limit', 40.4, 'Buy', 20000.49494338, 'GoodTillCancel'))

    # print(bitmex.place_order(bitmex.contracts['XBTUSD'], 'Limit', 50, 'Buy', price=20000, tif='GoodTillCancel'))

    root = tk.Tk()  # main win dow of the bot
    root.mainloop()  # blocking func that prevent program from terminating ('event loop' func - wait for action from user)
