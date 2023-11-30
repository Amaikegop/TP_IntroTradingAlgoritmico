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
        ("stop_loss_percent", 0.02)
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.bbands = bt.indicators.BollingerBands(period=self.params.bb_period, devfactor=self.params.bb_dev)
        self.body_size_threshold = 0.4


    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('GANANCIA DE LA OPERACION, Bruto: %.2f , Neto: %.2f' %
                 (trade.pnl,trade.pnlcomm))
        
    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(f"Compra completada - Precio: {order.executed.price}, Costo: {order.executed.price * order.executed.size}, Comisión: {order.executed.comm}")
            elif order.issell():
                self.log(f"Venta completada - Precio: {order.executed.price}, Ingreso: {order.executed.price * - order.executed.size}, Comisión: {order.executed.comm}")
        elif order.status in [order.Expired, order.Rejected]:
            self.log("La orden ha expirado o sido rechazada.")


    def next(self):
    
        if len(self) < 4:
            return
        three_white_soldiers = (
            self.data.close[-1] > self.data.open[-1] and #Alcista
            self.data.close[-2] > self.data.open[-2] and #Alcista
            self.data.close[-3] > self.data.open[-3] and #Alcista
            self.data.close[-1] > self.data.close[-2] and #la tercera cierra arriba que la segunda
            self.data.close[-2] > self.data.close[-3] and # la segunda cierra arriba de la primera
            self.data.open[-1] > self.data.open[-2] and # la tercera abre arriba de la segunda
            self.data.open[-2] > self.data.open[-3] and # la segunda abre arriba de la primera
            (self.data.close[-1] - self.data.open[-1]) > self.body_size_threshold * (self.data.high[-1] - self.data.low[-1]) and
            (self.data.close[-2] - self.data.open[-2]) > self.body_size_threshold * (self.data.high[-2] - self.data.low[-2]) and
            (self.data.close[-3] - self.data.open[-3]) > self.body_size_threshold * (self.data.high[-3] - self.data.low[-3])
        
        )

        if self.position.size == 0:
            amount_to_invest = self.params.order_porcentage * self.broker.cash
            self.size = math.floor((amount_to_invest / self.data.close))
            if three_white_soldiers:
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.rsi > self.params.overbought and self.data.close[0] >= self.bbands.lines.top[0] and not three_white_soldiers:
                self.sell(size=self.position.size)

            
