import logging

from models import *

logger = logging.getLogger()


class Strategy:
    def __init__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                 stop_loss: float):  # tp & sl in percentage
