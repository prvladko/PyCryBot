

class Balance:
    def __init__(self, info):
        self.initial_margin = float(info['initialMargin'])
        self.maintanance_margin = float(info['maintMargin'])
        self.margin_balance = float(info['marginBalance'])
        self.wallet_balance = float(info['walletBalance'])
        self.unrealized_pnl = float(info['unrealizedProfit'])