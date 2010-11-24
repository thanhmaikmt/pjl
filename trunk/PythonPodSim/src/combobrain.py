# converted to java  and then to python by p.j.leonard
# based  on C++ code found at 
# http://www.codeproject.com/KB/recipes/BP.aspx?msg=2809798#xx2809798xx

from math import  *
from random import  *
import copy
import pickle
import feedforwardbrain


def loadBrain(stream):
        # dummy to make compatible with backprop saved brains
        brain=ComboBrain()
        brain.net1=loadBrain()
        brain.net2=loadBrain()
        
        return brain
    
def breed(mum,dad):
    brain=ComboBrain()
    brain.net1=mum.net1.clone()
    brain.net2=dad.net2.clone()
    
    
    
class ComboBrain:
  
  
    def save(self,stream):
            net1.save(stream)
            net2.save(stream)
     
  
    
    def __init__(self,sz1=None,sz2=None):
        
        if sz1 != None and sz2 == None:
             #//    set no of layers and their sizes
            num_layer = len(sz1)
            layer_size = []   # new int[num_layer];

            for  i in range(num_layer-1):
                layer_size.append(sz1[i])

            layer_size.append(sz1[num_layer-1]/2)
            
            sz1=layer_size
            sz2=layer_size 
                
        if sz1 != None:
            self.net1=feedforwardbrain.FeedForwardBrain(sz1)
        if sz2 != None:
            self.net2=feedforwardbrain.FeedForwardBrain(sz2)

    
        
    def clone(self):
        clone=ComboBrain()
        clone.net1=self.net1.clone()
        clone.net2=self.net2.clone()
        return clone

    
    def mutate(self,amount):
        # mutate net1 or net2
        self.net1.mutate(amount)
        self.net2.mutate(amount)     
        
        
    #  feed forward one set of input
    def ffwd(self,x):
        
        
        out=self.net1.ffwd(x)
        out2=self.net2.ffwd(x)
            
        out.extend(out2)
        
        return out
    
    
            
            