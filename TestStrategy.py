import backtrader as bt

class TestStrategy(bt.Strategy): #Tres soldados blancos
    params = (
        ("umbral_sombra_superior", 0.2),  # Umbral para considerar la sombra superior como pequeña
        ("umbral_sombra_inferior", 0.2),  # Umbral para considerar la sombra inferior como pequeña
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.ultima_cierre = self.datas[0].close
        self.patron_detectado = False
        self.patron_detectado

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            # Restablecer después de cada operación
            self.patron_detectado = False

    def next(self):
        if len(self) < 2:
            return

        open_actual = self.data.open[0]
        high_actual = self.data.high[0]
        low_actual = self.data.low[0]
        close_actual = self.data.close[0]

        print('open high ', high_actual)

        cuerpo_actual = abs(open_actual - close_actual)
        sombra_superior = high_actual - max(open_actual, close_actual)
        sombra_inferior = min(open_actual, close_actual) - low_actual

        es_martillo = (
            cuerpo_actual < sombra_superior * self.params.umbral_sombra_superior
            and cuerpo_actual < sombra_inferior * self.params.umbral_sombra_inferior
        )

        if es_martillo and not self.patron_detectado:
            self.patron_detectado = True
            self.log("Patrón Martillo detectado. Comprar.")

            # Establecer la orden de compra
            self.buy()