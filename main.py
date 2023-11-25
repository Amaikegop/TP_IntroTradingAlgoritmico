from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import TestStrategy

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'orcl-1995-2014.txt')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(1995, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2014, 12, 31),
        reverse=False,
        adjclose = False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    cerebro.broker.setcommission(commission=0.001)
    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # strategy = TestStrategy()
    cerebro.addstrategy(TestStrategy.TestStrategy)
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    for data in cerebro.datas:
        print('Símbolo:', data._name, 'Posición:', cerebro.broker.getposition(data).size)
    
    def plot(self, fig, plotter):
        # Agregar líneas para visualizar las medias móviles corta y larga
        plotter.plotline(self.sma_short, color='green', linewidth=2, linestyle='dashed', subplot=True)
        plotter.plotline(self.sma_long, color='red', linewidth=2, linestyle='dashed', subplot=True)
        # Marcar las señales de compra y venta con triángulos
    
    # cerebro.plot()