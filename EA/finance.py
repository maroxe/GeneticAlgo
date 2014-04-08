from random import choice

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical  import ma, rsi
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns

from matplotlib import pyplot as plt
import ga
import rules

filename = "resources/finance/orcl-2000.csv"
instrument = "orcl"

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, rule):
        strategy.BacktestingStrategy.__init__(self, feed, 1000)
        self.setUseAdjustedValues(True)
        
        self.__feed = feed
        self.__ticks = feed[instrument].getAdjCloseDataSeries()
        self.__sma = ma.SMA(self.__ticks, 15)

        self.__instrument = instrument
        self.__position = None
        self.__rule = rule
    
    def getSMA2(self):
        return self.__sma     
       
    def getSMA(self, period):
        return sum(self.__ticks[-period:]) / period

        
    def getMax(self, period):
        return max(self.__ticks[-period:])
        
    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        #self.info('BUY at %.2f' % execInfo.getPrice())
            
    def onEnterCanceled(self, position):
        self.debug('Enter canceled')
        self.__position = None
    
    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        #self.info('SELL at %.2f' % execInfo.getPrice())
        self.__position = None
        
    def onExitCanceled(self, position):
        self.debug('Exit canceled')
        self.__position.exitMarket()
        
    def onBars(self, bars):
        if self.__position is None:
            if self.__rule.eval():
                self.__position = self.enterLong(self.__instrument, 10, True)
        elif not self.__rule.eval():
            self.__position.exitMarket()

n = 10

    
def fitness(rule):
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, filename)
    strat = MyStrategy(feed, instrument, rule)
    rules.strategy = strat
    
    #plt = plotter.StrategyPlotter(strat)
    #plt.getInstrumentSubplot("orcl").addDataSeries("SMA", strat.getSMA2())
    strat.run()
    #print 'gain = %2.f$' % (strat.getResult() - 1000) 

    # plt.plot()
    #print strat.getResult()-1000
    return strat.getResult()-1000

def mutation(l, x):
    x_mut = x.copy()
    for _ in range(l*10):
        node = choice(x_mut.nodes()).parent
        if node == None:
            x_mut = rules.generate_bool(n)
        else:
            node.mutate_child(10)
    return x_mut

def crossover(c, x, xx):
    x_cross = x.copy()
    #for _ in range(int(len(x) * c) + 1):
    for _ in range(int(c*10)):
        node_to_replace = choice(x_cross.nodes())
        parent = node_to_replace.parent
        
        if parent == None:
            return rules.generate_bool(n)
            
        same_type_nodes = filter(lambda n: n.type() == node_to_replace.type(), xx.nodes())
        try:
            node_to_add = choice(same_type_nodes).copy()
            parent.replace_child(node_to_replace, node_to_add)
        except IndexError:
            #print 'warning no node matches'
            pass
    return x_cross

x_init = rules.generate_bool(n)
rules.draw_tree(x_init, "resources/finance/init.png")
ea_algo = ga.EA(fitness=fitness, mutation=mutation, crossover=crossover)
best_x = ea_algo.run(n, x_init, offspring_size=8, n_generations=10000, p=0.5, c=0.5)
rules.draw_tree(best_x, "resources/finance/beststrat.png")
print 'best = ', fitness(best_x)


    