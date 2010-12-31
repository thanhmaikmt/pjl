import feedforwardbrain as brain
from random import *



class BrainPlug:

    CAN_BREED=True
    
    def __init__(self,sz):
        self.layerSizes=sz
        
    def loadBrain(self,file):
        return brain.loadBrain(file)
    
    def createBrain(self):
        return brain.FeedForwardBrain(self.layerSizes)
        
    def breed(self,mum,dad):
        
        child=mum.clone()
        for i in range(1,child.num_layer):  
            a=child.weight[i]
            d=dad.weight[i]
            
            n=child.layer_size[i]
            
            split=randrange(n+1)
            #print "split",split
            for j in range(split,n):
                childW=a[j]
                dW=d[j]
                
                for k in range(child.layer_size[i - 1]+1):
                    childW[k]=dW[k]
                    
                    
        return child
    
    def mutate(self,brain,amount):
        brain.mutate(amount)