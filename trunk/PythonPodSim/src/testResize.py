'''
Created on 15 Dec 2010

@author: pjl
'''


import feedforwardbrain 



sz=[2,3,1]

brain=feedforwardbrain.FeedForwardBrain(sz)


print brain.weight

brain.resize_inputs(4)

print brain.weight
print brain.layer_size

brain.mutate(100.0)


print brain.weight
