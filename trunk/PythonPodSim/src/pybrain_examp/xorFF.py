from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.structure.modules.tanhlayer import TanhLayer
from pybrain.structure.modules import SoftmaxLayer

net=buildNetwork(2,2,1,outclass=SigmoidLayer)
net.sortModules()

print net

from pybrain.datasets import SupervisedDataSet

ds = SupervisedDataSet(2, 1)

ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (0,))


from pybrain.supervised.trainers import BackpropTrainer


def testNet():
    for x,t in zip(ds['input'],ds['target']):
        y=net.activate(x)
        print x,t,y

#net = buildNetwork(2, 3, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds,.6) #,.01,momentum=.01,verbose=True,weightdecay=0.01)  # ,.01,1.0,0)

tol=0.5*.25*.25/4.0
print tol

count=0
for i in range(5000):
    count +=1
    val=trainer.train()
    print count,val
    testNet()

    if val < tol:
        break
