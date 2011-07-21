from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer

from pybrain.datasets import SupervisedDataSet, ImportanceDataSet


class SequentialXORDataSet(ImportanceDataSet):
    """ same thing, but sequential, and having no importance on a second output"""
    def __init__(self):
        ImportanceDataSet.__init__(self, 2, 2)
        self.addSample([0,0],[0, 1],  [1,0])
        self.addSample([0,1],[1, 10], [1,0])
        self.addSample([1,0],[1, -1], [1,0])
        self.addSample([1,1],[0, 0],  [1,0])


d = SequentialXORDataSet()
n = buildNetwork(d.indim, 4, d.outdim, recurrent=True)
t = BackpropTrainer(n, learningrate = 0.01, momentum = 0.99, verbose = True)
t.trainOnDataset(d, 1000)
t.testOnData(verbose= True)
