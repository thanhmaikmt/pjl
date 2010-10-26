# converted to java  and then to python by p.j.leonard
# based  on C++ code found at 
# http://www.codeproject.com/KB/recipes/BP.aspx?msg=2809798#xx2809798xx

from math import  *
from random import  *

def sigmoid(x):
        return 1.0 / (1.0 + exp(-x))
    
def randomSeed():
    return 0.5 - random()

class BackPropBrain:
    
    
    def __init__(self,sz, b, a):


        self.beta = b
        self.alpha = a

        #//	set no of layers and their sizes
        self.numl = len(sz)
        self.lsize = []   # new int[numl];

        for  i in range(self.numl):
            self.lsize.append(sz[i])
        

        #//	allocate memory for output of each neuron
        self.out = [] # new float[numl][];
        for  i in range(self.numl):  
            self.out.append([]);
            a=self.out[i]
            for k in range(self.lsize[i]):
                a.append(0.0)

        
        self.delta = []
        for  i in range(self.numl):  
            self.delta.append([]);
            a=self.delta[i]
            for k in range(self.lsize[i]):
                a.append(0.0)


        self.weight=[]
        self.weight.append([])
        
        for i in range(1,self.numl):  
            self.weight.append([])
            a=self.weight[i]
            for j in range(self.lsize[i]):
                a.append([])
                r=a[j]
                for k in range(self.lsize[i - 1]):
                    r.append(randomSeed())
                r.append(randomSeed())
    
        self.prevDwt=[]
        self.prevDwt.append([])
        
        for i in range(1,self.numl):  
            self.prevDwt.append([])
            a=self.prevDwt[i]
            for j in range(self.lsize[i]):
                a.append([])
                r=a[j]
                for k in range(self.lsize[i - 1]):   
                    r.append(0.0)
                r.append(0.0)
        
#//  I did this intentionaly to maintains consistancy in numbering the layers.
#//  Since for a net having n layers, input layer is refered to as 0th layer,
#//  first hidden layer as 1st layer and the nth layer as output layer. And 
#//  first (0th) layer just stores the inputs hence there is no delta or weigth
#//  values corresponding to it.
 
 
    def output(self):
        return self.out[self.numl - 1];
    
    
    def input(self):
        return self.out[0];
    
    
    # mean square error
    def mse(self,tgt): 
        mse = 0.0;
        for i in range(self.lsize[self.numl - 1]):
             mse += (tgt[i] - self.out[self.numl - 1][i]) * (tgt[i] - self.out[self.numl - 1][i]);
        
        return mse / 2.0;
   

    #  feed forward one set of input
    def ffwd(self,x):
        
        #	assign content to input layer
        for  i in range(self.lsize[0]):
                 self.out[0][i] = x[i]       # output_from_neuron(i,j) Jth neuron in Ith Layer

        #	assign output(activation) value 
        #	to each neuron usng sigmoid func
        
        for i in range(1,self.numl):         #  For each layer
            for j in range(self.lsize[i]):   #  For each neuron in current layer
                sum = 0.0;
                for k  in range(self.lsize[i - 1]):                     # For input from each neuron in preceeding layer
                    sum += self.out[i - 1][k] * self.weight[i][j][k];	# Apply weight to inputs and add to sum
                
                sum += self.weight[i][j][self.lsize[i - 1]];	    	# Apply bias
                self.out[i][j] = sigmoid(sum);				            # Apply sigmoid function
    
        return self.out[self.numl - 1];
    
    #	backpropogate errors from output.
    #   modify weights
    def bpgt(self,x, tgt):
        
        #	update output values for each neuron
        self.ffwd(x);

        #    find delta for output layer
        for i in range(self.lsize[self.numl - 1]):  
            self.delta[self.numl - 1][i] = self.out[self.numl - 1][i] * \
                    (1 - self.out[self.numl - 1][i]) * (tgt[i] - self.out[self.numl - 1][i])
        

        #   find delta for hidden layers	
        for i in range(self.numl-2,0,-1) : 
            for  j  in range(self.lsize[i]):
                sum = 0.0;
                for k in range(self.lsize[i + 1]):
                    sum += self.delta[i + 1][k] * self.weight[i + 1][k][j];
                
                self.delta[i][j] = self.out[i][j] * (1 - self.out[i][j]) * sum;
         
         
        #	apply momentum ( does nothing if alpha=0 )
        for i in range(1,self.numl):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i - 1]):
                    self.weight[i][j][k] += self.alpha * self.prevDwt[i][j][k];
                
                self.weight[i][j][self.lsize[i - 1]] += self.alpha * self.prevDwt[i][j][self.lsize[i - 1]];
            
        #	adjust weights using steepest descent	
        for i in range(1,self.numl):
            for j in range(self.lsize[i]):
                for  k in range(self.lsize[i - 1]):
                    self.prevDwt[i][j][k] = (float) (self.beta * self.delta[i][j] * self.out[i - 1][k]);
                    self.weight[i][j][k] += self.prevDwt[i][j][k];
                
                self.prevDwt[i][j][self.lsize[i - 1]] = (float) (self.beta * self.delta[i][j]);
                self.weight[i][j][self.lsize[i - 1]] += self.prevDwt[i][j][self.lsize[i - 1]];
    
   