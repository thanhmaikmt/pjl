# converted to java  and then to python by p.j.leonard
# based  on C++ code found at 
# http://www.codeproject.com/KB/recipes/BP.aspx?msg=2809798#xx2809798xx

from math import  *
from random import  *
import copy
import pickle

def sigmoid(x):
        if x < -100:
            return 0.0
        
        return 1.0 / (1.0 + exp(-x))
    
def randomSeed():
    return 0.5 - random()

def loadBrain(stream):
        b=pickle.load(stream)
        a=pickle.load(stream)
        sz=pickle.load(stream)
        brain=BackPropBrain(sz, b, a) 
        brain.weight=pickle.load(stream)    
        return brain
    
    
class BackPropBrain:
  
  
    def save(self,stream):
            bb=copy.deepcopy(self.beta)
            pickle.dump(bb,stream)
            
            aa=copy.deepcopy(self.alpha)  
            pickle.dump(aa,stream)
            
            ssz=copy.deepcopy(self.layer_size)
            pickle.dump(ssz,stream)
            
            w=copy.deepcopy(self.weight)
            pickle.dump(w,stream)
    
  
    
    def __init__(self,sz, b=.001, a=10):

        self.beta = b
        self.alpha = a

        #//	set no of layers and their sizes
        self.num_layer = len(sz)
        self.layer_size = []   # new int[num_layer];

        for  i in range(self.num_layer):
            self.layer_size.append(sz[i])

 
        #//	allocate memory for output of each neuron
        self.out = [] # new float[num_layer][];
        for  i in range(self.num_layer):  
            self.out.append([]);
            a=self.out[i]
            for k in range(self.layer_size[i]):
                a.append(0.0)

        
        self.delta = []
        for  i in range(self.num_layer):  
            self.delta.append([]);
            a=self.delta[i]
            for k in range(self.layer_size[i]):
                a.append(0.0)


        self.weight=[]
        self.weight.append([])
        
        for i in range(1,self.num_layer):  
            self.weight.append([])
            a=self.weight[i]
            for j in range(self.layer_size[i]):
                a.append([])
                r=a[j]
                for k in range(self.layer_size[i - 1]):
                    r.append(randomSeed())
                r.append(randomSeed())
    
        self.prevDwt=[]
        self.prevDwt.append([])
        
        for i in range(1,self.num_layer):  
            self.prevDwt.append([])
            a=self.prevDwt[i]
            for j in range(self.layer_size[i]):
                a.append([])
                r=a[j]
                for k in range(self.layer_size[i - 1]):   
                    r.append(0.0)
                r.append(0.0)
        
        
    def clone(self):
        clone=BackPropBrain(self.layer_size,self.alpha,self.beta)
        clone.weight=copy.deepcopy(self.weight)
        return clone
            
    def mutate(self,amount):    
        for i in range(1,self.num_layer):
            a=self.weight[i]  
            for j in range(self.layer_size[i]):            
                r=a[j]
                for k in range(self.layer_size[i]):
                    r[k]=r[k]+randomSeed()*amount
                    
        
            
#//  I did this intentionaly to maintains consistancy in numbering the layers.
#//  Since for a net having n layers, input layer is refered to as 0th layer,
#//  first hidden layer as 1st layer and the nth layer as output layer. And 
#//  first (0th) layer just stores the inputs hence there is no delta or weigth
#//  values corresponding to it.
 
 
    def output(self):
        return self.out[self.num_layer - 1];
    
    
    def input(self):
        return self.out[0];
    
    
    # mean square error
    def mse(self,tgt): 
        mse = 0.0;
        for i in range(self.layer_size[self.num_layer - 1]):
             mse += (tgt[i] - self.out[self.num_layer - 1][i]) * (tgt[i] - self.out[self.num_layer - 1][i]);
        
        return mse / 2.0;
   

    #  feed forward one set of input
    def ffwd(self,x):
        
        #	assign content to input layer
        for  i in range(self.layer_size[0]):
                 self.out[0][i] = x[i]       # output_from_neuron(i,j) Jth neuron in Ith Layer

        #	assign output(activation) value 
        #	to each neuron usng sigmoid func
        
        for i in range(1,self.num_layer):         #  For each layer
            for j in range(self.layer_size[i]):   #  For each neuron in current layer
                sum = 0.0;
                for k  in range(self.layer_size[i - 1]):                     # For input from each neuron in preceeding layer
                    sum += self.out[i - 1][k] * self.weight[i][j][k];	# Apply weight to inputs and add to sum
                
                sum += self.weight[i][j][self.layer_size[i - 1]];	    	# Apply bias
                self.out[i][j] = sigmoid(sum);				            # Apply sigmoid function
    
        return self.out[self.num_layer - 1];
    
    #	backpropogate errors from output.
    #   modify weights
    def bpgt(self,x, tgt):
        
        #	update output values for each neuron
        self.ffwd(x);

        #    find delta for output layer
        for i in range(self.layer_size[self.num_layer - 1]):  
            self.delta[self.num_layer - 1][i] = self.out[self.num_layer - 1][i] * \
                    (1 - self.out[self.num_layer - 1][i]) * (tgt[i] - self.out[self.num_layer - 1][i])
        

        #   find delta for hidden layers	
        for i in range(self.num_layer-2,0,-1) : 
            for  j  in range(self.layer_size[i]):
                sum = 0.0;
                for k in range(self.layer_size[i + 1]):
                    sum += self.delta[i + 1][k] * self.weight[i + 1][k][j];
                
                self.delta[i][j] = self.out[i][j] * (1 - self.out[i][j]) * sum;
         
         
        #	apply momentum ( does nothing if alpha=0 )
        for i in range(1,self.num_layer):
            for j in range(self.layer_size[i]):
                for k in range(self.layer_size[i - 1]):
                    self.weight[i][j][k] += self.alpha * self.prevDwt[i][j][k];
                
                self.weight[i][j][self.layer_size[i - 1]] += self.alpha * self.prevDwt[i][j][self.layer_size[i - 1]];
            
        #	adjust weights using steepest descent	
        for i in range(1,self.num_layer):
            for j in range(self.layer_size[i]):
                for  k in range(self.layer_size[i - 1]):
                    self.prevDwt[i][j][k] = (float) (self.beta * self.delta[i][j] * self.out[i - 1][k]);
                    self.weight[i][j][k] += self.prevDwt[i][j][k];
                
                self.prevDwt[i][j][self.layer_size[i - 1]] = self.beta * self.delta[i][j];
                self.weight[i][j][self.layer_size[i - 1]] += self.prevDwt[i][j][self.layer_size[i - 1]];
    
        return self.mse(tgt)
            
            
            