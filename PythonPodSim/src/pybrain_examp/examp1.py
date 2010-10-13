from pybrain.tools.shortcuts import buildNetwork


net=buildNetwork(2,1)
net.sortModules()



# print values  [bias, w0,w2]

w=net.params

print w

net._setParameters([1,2,3,4,5,6,7,8])
# activate with zeros
val=net.activate([0,0,0])

# val should be the same as the first weight
print val

