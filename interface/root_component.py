import tkinter as tk

from connectors.bitmex import BitmexClient
from connectors.binance_futures import BinanceFuturesClient

from interface.styling import *
from interface.logging_component import Logging
from interface.watchlist_component import Watchlist

class Root(tk.Tk):  # пример ООП наследования (inheritance)
    def __init__(self, binance: BinanceFuturesClient, bitmex: BitmexClient):
        super().__init__()

        self.binance = binance
        self.bitmex = bitmex

        self.title('Trading Bot')

        self.configure(bg=BG_COLOR)

        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side=tk.LEFT)

        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side=tk.LEFT)

        self._watchlist_frame = Watchlist(self.binance.contracts, self.bitmex.contracts, self._left_frame, bg=BG_COLOR)
        self._watchlist_frame.pack(side=tk.TOP)

        self._logging_frame = Logging(self._left_frame, bg=BG_COLOR)
        self._logging_frame.pack(side=tk.TOP)

        self._update_ui()

        # self._logging_frame.add_log('This is test message')
        # time.sleep(2)
        # self._logging_frame.add_log('This is another test message')

    def _update_ui(self):

        # Logs

        for log in self.bitmex.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        for log in self.binance.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        # Watchlist prices

        for key, value in self._watchlist_frame.body_widgets['symbol'].items():

            symbol = self._watchlist_frame.body_widgets['symbol'][key].cget('text')
            exchange = self._watchlist_frame.body_widgets['exchange'][key].cget('text')

            if exhcange == 'Binance':
                if symbol not in self.binance.contracts:
                    continue

                if symbol not in self.binance.prices:
                    self.binance.get_bid_ask(self.binance.contracts[symbol])
                    continue

                prices = self.binance.prices(symbol)

            elif exhcange == 'Bitmex':
                if symbol not in self.bitmex.contracts:
                    continue

                if symbol not in self.bitmex.prices:
                    continue

                prices = self.binance.prices(symbol)

            else:
                continue

            if prices['bid'] is not None:
                self._watchlist_frame.body_widgets['bid_var'][key].set(prices['bid'])
            if prices['ask'] is not None:
                self._watchlist_frame.body_widgets['ask_var'][key].set(prices['ask'])









        self.after(1500, self._update_ui)