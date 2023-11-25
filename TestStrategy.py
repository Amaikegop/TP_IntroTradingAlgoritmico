import backtrader as bt

class TestStrategy(bt.Strategy):
    params = (
        #Patron de velas velas: Martillo
        ("umbral_sombra_superior", 0.2),  # Umbral para considerar la sombra superior como pequeña
        ("umbral_sombra_inferior", 0.2),  # Umbral para considerar la sombra inferior como pequeña
        
        #Golden cross
        ("sma_short", 50),  # Período de la media móvil corta
        ("sma_long", 200),   # Período de la media móvil larga
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.ultimo_cierre = self.datas[0].close
        self.patron_martillo_detectado = False
        self.golden_gross_detectado_buy = False
        self.golden_gross_detectado_sell = False
        self.sma_short = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.sma_short)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.sma_long)
    
    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            # Restablecer después de cada operación
            if (self.patron_martillo_detectado and self.golden_gross_detectado_buy):
                self.patron_martillo_detectado = False
                self.golden_gross_detectado_buy = False
            elif (self.golden_gross_detectado_sell):
                self.golden_gross_detectado_sell = False
            self.log("Orden completada. Restableciendo.")

    def next(self):
        # self.log('Close, %.2f' % self.ultimo_cierre[0])
        # if len(self) < 2:
        #     return
        
        open_actual =self.datas[0].open
        high_actual = self.datas[0].high
        low_actual = self.datas[0].low
        close_actual = self.datas[0].close

        cuerpo_actual = abs(open_actual - close_actual)
        sombra_superior = high_actual - max(open_actual, close_actual)
        sombra_inferior = min(open_actual, close_actual) - low_actual

        es_martillo = (
            cuerpo_actual < sombra_superior * self.params.umbral_sombra_superior
            and cuerpo_actual < sombra_inferior * self.params.umbral_sombra_inferior
        )
        # print('la de 50:',self.sma_short[0])
        # print('la de 200:',self.sma_long[0])

        size = int(self.broker.cash / self.datas[0].close)
        #Golden cross
        if (self.sma_short[0] > self.sma_long[0]) and not self.golden_gross_detectado_buy and (es_martillo and not self.patron_martillo_detectado):
            self.log("Estrategia detectada. Comprar.")

            # Establecer la orden de compra
            self.buy()

            # Establecer el stop loss
            # stop_loss_price = self.data.close * 0.98  # Por ejemplo, un 2% por debajo del cierre actual
            # self.sell(
            #     size=size,
            #     price=stop_loss_price,
            #     exectype=bt.Order.Stop,
            #     parent=self.buy_order
            # )
            
            self.patron_martillo_detectado = True
            self.golden_gross_detectado_buy = True
        
        if (self.sma_short[0] < self.sma_long[0]) and not self.golden_gross_detectado_sell:
            self.log("Estrategia detectada. Vender.")
            # print(self.position)
            # if (self.position):     ##ver porque no anda
            self.sell()

            self.golden_gross_detectado_sell = True
