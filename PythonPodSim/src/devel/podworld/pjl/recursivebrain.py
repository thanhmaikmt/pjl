
from feedforwardbrain import *

class RecursiveBrain(FeedForwardBrain):


    def __init__(self,sz,func=[None,sigmoid,sigmoid],weight=None):
        self.nIn=sz[0]
        sss = copy.deepcopy(sz)
        sss[0]= sss[0]+sss[1]
        FeedForwardBrain.__init__(self,sss,func,weight)
        
    def clone(self):
        sss=copy.deepcopy(self.layer_size)
        sss[0]=sss[0]-sss[1]
        weight=copy.deepcopy(self.weight)
        clone=RecursiveBrain(sss,self.func,weight)
        assert clone.dist(self) == 0.0
        
        return clone     
        

    #  feed forward one set of input
    def ffwd(self,x):
        
       # print len(x),self.nIn
        assert len(x) == self.nIn
        
        #    assign content to input layer
        for  i in range(self.nIn):
            self.out[0][i] = x[i]       # output_from_neuron(layer,j) Jth neuron in Ith Layer
        
        for i in range(self.layer_size[1]):
             self.out[0][self.nIn+i] = self.out[0][i]
        
        #    assign output(activation) value 
        #    to each neuron using sigmoid func
        
        for layer in range(1,self.num_layer):         #  For each layer
            for j in range(self.layer_size[layer]):   #  For each neuron in current layer
                sum = 0.0;
                for k  in range(self.layer_size[layer - 1]):                     # For input from each neuron in preceeding layer
                    sum += self.out[layer - 1][k] * self.weight[layer][j][k];    # Apply weight to inputs and add to sum
                
                sum += self.weight[layer][j][self.layer_size[layer - 1]];            # Apply bias
                self.out[layer][j] = self.func[layer](sum);                            # Apply sigmoid function
    
        return self.out[self.num_layer - 1];
        
        
        
        
        
        
        