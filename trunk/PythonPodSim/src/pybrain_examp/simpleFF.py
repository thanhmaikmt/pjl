from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.structure.modules.tanhlayer import TanhLayer

net=buildNetwork(2,1,outclass=SigmoidLayer)
net.sortModules()

print net

from pybrain.datasets import SupervisedDataSet

ds = SupervisedDataSet(2, 1)

ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (1,))


from pybrain.supervised.trainers import BackpropTrainer


def testNet():
    for x,t in zip(ds['input'],ds['target']):
        y=net.activate(x)
        print x,t,y

#net = buildNetwork(2, 3, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds,.01,1.0,1)

for i in range(500):
    testNet()
    print trainer.train()
