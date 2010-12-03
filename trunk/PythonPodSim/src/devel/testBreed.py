'''
Created on 3 Dec 2010

@author: pjl
'''


import gravityPlug
import feedforwardbrain


def printOutWeights(brain):
    print " Layer size (input  hidden  . . .  output : ",
    for n in brain.layer_size:
        print n," ",

            
    #  For each layer
    for i in range(1,brain.num_layer):         
        print " conections to layer ",i
        
        #  For each neuron in current layer
        for j in range(brain.layer_size[i]):   
           
            # For input from each neuron in preceeding layer
            # NOTE: bias connection is weight[i][j][brain.layer_size[i - 1]]
            # this is not included in the count so we have to have +1  
            for k  in range(brain.layer_size[i - 1]+1):
                    print brain.weight[i][j][k]," ",
            print

plug=gravityPlug.GravityPlug()


ls=[1,2]

mum=feedforwardbrain.FeedForwardBrain(ls)
dad=mum.clone()
#printOutWeights(mum)

dad.mutate(1.0)

child=plug.bread(mum, dad)

print mum.weight

print dad.weight

print child.weight
