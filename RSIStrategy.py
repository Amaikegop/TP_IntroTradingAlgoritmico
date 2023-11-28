import backtrader as bt
import math

class BollingerRSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('bb_period', 20),
        ('bb_dev', 2),
        ('oversold', 30),
        ('overbought', 70),
        ('order_porcentage', 0.95),
        ('ticker','PSY')
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.bbands = bt.indicators.BollingerBands(period=self.params.bb_period, devfactor=self.params.bb_dev)

    
    def next(self):
        date = self.datas[0].datetime.date(0)

        if self.position.size == 0:
            if self.rsi < self.params.oversold and self.data.close[0] <= self.bbands.lines.bot[0]:
                amount_to_invest = self.params.order_porcentage * self.broker.cash
                self.size = math.floor(amount_to_invest / self.data.close)

                print(f'{date}: Buy {self.size} shares of {self.params.ticker} at {self.data.close[0]:.2f}.')
                self.buy(size=self.size)
        
        if self.position.size > 0:
            if self.rsi > self.params.overbought or self.data.close[0] >= self.bbands.lines.top[0]:
                print(f'{date}: Sell {self.size} shares of {self.params.ticker} at {self.data.close[0]:.2f}.\n')
                self.close()