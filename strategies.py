import logging

from models import *

logger = logging.getLogger()


class Strategy:
    def __init__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                 stop_loss: float):  # tp & sl in percentage

        self.contract = contract
        self.exchange = exchange
        self.tf = timeframe
        self.balance_pct = balance_pct
        self.take_profit = take_profit
        self.stop_loss = stop_loss


class TechnicalStrategy(Strategy):
    def __init__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                 stop_loss: float, other_params):  # other_params for example ema_fast