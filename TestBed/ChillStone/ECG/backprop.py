# converted to java  and then to python by p.j.leonard
# based  on C++ code found at 
# http://www.codeproject.com/KB/recipes/BP.aspx?msg=2809798#xx2809798xx

import math
import random
import copy


#
# multilayer neural network with backprop training
#     
 
def sigmoid(x):
        if x < -100:        #  stops function blowing up !!!!
            return 0.0
    
        return 1.0 / (1.0 + math.exp(-x))
    
def randomSeed():
    return 0.5 - random.random()

    
class BackPropBrain:
  
  

    def __init__(self,sz, beta=.01, alpha=100):
        """ Create a neural net
            sz is  list that defines the number neurons in each layer
            beta is the learning rate
            alpha is the momentum
            """ 
        
        self.beta = beta
        self.alpha = alpha

        # set no of layers and their sizes
        self.num_layer = len(sz)
        self.layer_size = []   

        for  i in range(self.num_layer):
            self.layer_size.append(sz[i])

 
        #  allocate memory for output of each neuron
        self.out = []
        for  i in range(self.num_layer):  
            self.out.append([]);
            a=self.out[i]
            for _ in range(self.layer_size[i]):
                a.append(0.0)

        
        self.delta = []
        for  i in range(self.num_layer):  
            self.delta.append([]);
            a=self.delta[i]
            for _ in range(self.layer_size[i]):
                a.append(0.0)


        self.weight=[]
        self.weight.append([])
        
        for i in range(1,self.num_layer):  
            self.weight.append([])
            a=self.weight[i]
            for j in range(self.layer_size[i]):
                a.append([])
                r=a[j]
                for _ in range(self.layer_size[i - 1]):
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
                for _ in range(self.layer_size[i - 1]):   
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
                for k in range(self.layer_size[i-1]+1):
                    r[k]=r[k]+randomSeed()*amount
 
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
        
        #    assign content to input layer
        for  i in range(self.layer_size[0]):
            self.out[0][i] = x[i]       # output_from_neuron(i,j) Jth neuron in Ith Layer

        #    assign output(activation) value 
        #    to each neuron usng sigmoid func
        
        for i in range(1,self.num_layer):         #  For each layer
            for j in range(self.layer_size[i]):   #  For each neuron in current layer
                sum = 0.0;
                for k  in range(self.layer_size[i - 1]):                     # For input from each neuron in preceeding layer
                    sum += self.out[i - 1][k] * self.weight[i][j][k];    # Apply weight to inputs and add to sum
                
                sum += self.weight[i][j][self.layer_size[i - 1]];            # Apply bias
                self.out[i][j] = sigmoid(sum);                            # Apply sigmoid function
    
        return self.out[self.num_layer - 1];
    
    #    backpropogate errors from output.
    #   modify weights
    def bpgt(self,x, tgt):
        
        #    update output values for each neuron
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
         
         
        #    apply momentum ( does nothing if alpha=0 )
        for i in range(1,self.num_layer):
            for j in range(self.layer_size[i]):
                for k in range(self.layer_size[i - 1]):
                    self.weight[i][j][k] += self.alpha * self.prevDwt[i][j][k];
                
                self.weight[i][j][self.layer_size[i - 1]] += self.alpha * self.prevDwt[i][j][self.layer_size[i - 1]];
            
        #    adjust weights using steepest descent    
        for i in range(1,self.num_layer):
            for j in range(self.layer_size[i]):
                for  k in range(self.layer_size[i - 1]):
                    self.prevDwt[i][j][k] = (float) (self.beta * self.delta[i][j] * self.out[i - 1][k]);
                    self.weight[i][j][k] += self.prevDwt[i][j][k];
                
                self.prevDwt[i][j][self.layer_size[i - 1]] = self.beta * self.delta[i][j];
                self.weight[i][j][self.layer_size[i - 1]] += self.prevDwt[i][j][self.layer_size[i - 1]];
    
        return self.mse(tgt)
            
            
            

if __name__ == "__main__":
    
    
    n_in=2
    n_hid=2
    n_out=2
    
    # test the net and return an error estimate
    def test_net(nn,training_in,training_out):
        error=0.0
        for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
            out=nn.ffwd(x)
            for t,o in zip(target,out):
                error += math.fabs(t-o)
            
        return error
    
    
    
    # test the net and return an error estimate
    def train_net(nn,training_in,training_out):
        for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
            nn.bpgt(x,target)
      
    
    # test the net and return an error estimate
    def test_net_print(nn,training_in,training_out):
        error=0.0
        for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
            out=nn.ffwd(x)
            print x,"|",target,"|",out
            
        return error
    
    
    # create a NeuralNet that we will try to optimize for the following training data
    nn=BackPropBrain([n_in,n_hid,n_out])
    
    
    # XOR training data
    
    training_in=[[0,0],[0,1],[1,0],[1,1]]
    training_out=[[0,1],[1,0],[1,0],[0,1]]
    
    
    MAX_ITERS = 100000
    
    #print guess
    
    TOL=0.1
    best_error=1e32
    iter=0
    
    while iter < MAX_ITERS:
    
        train_net(nn,training_in,training_out)
        error=test_net(nn,training_in,training_out)
        
        if error < best_error:
            best_error=error
            print iter,error
       
        if error <= TOL:
            break
             
        iter += 1
    
    
    success=best_error <= TOL
    
    if success:
        print " Success ", " Iters ",iter,"\n"
    
    else:
        print " Failed", " best error=",best_error
    
    
    test_net_print(nn,training_in,training_out)