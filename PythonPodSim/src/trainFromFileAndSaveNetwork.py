#
#   Test for BackPropBrain
#
#   I find that sometimes this does not converge (possibly stuck in local a minimum)
#
#   When it does converge it takes about 2000 iterations
#   
#   Each run starts with random weights so just keep trying until it does converge.


from backpropbrain import *


def readTrainingData(file,nin,nout):
    TD=[]
    
    while True:
        line=file.readline()
        if len(line) == 0:
            return TD
        
        toks=line.split()
    
        input = []
        for i in range(nin):
            input.append(float(toks[i]))
            
        output = []
        for i in range(nin,nin+nout):
            output.append(float(toks[i]))
            
        TD.append([input,output])
        
    
    

#  Use your own numbers here
ninputs =9 
nhidden =6
nout    =4   

 
file=open("carTraining.txt","r")

TD = readTrainingData(file,ninputs,nout)

#print TD

layerSizes = [ninputs, nhidden, nout]


# These make a lot of difference
# I found these by trail and error.
beta = .1    # learning rate
alpha = 10.0    # momentum

#Create a brain
brain =BackPropBrain(layerSizes, beta, alpha)

iter=0
maxIter=20000

# acceptable error  = 1/2 SUM error_i*error_i
# for a real / noisy data set this may be too big.
# you will need to experiment with this value
tol = 0.0001     
                     
# these are used to accelerated search once error starts to fall
dodecay=True                # switch off by setting this to False
decayFact=.995
errorlast=0.0

#
#   now loop until convergence.
#

while True:   # loop until happiness is found or we exceed maxIter 
    
    iter += 1
    error= 0.0      # 
        
        
    error=0.0
        
    for td in TD:  # loop on all the training data
        error1=brain.bpgt(td[0],td[1])     # train for one data set. 
        error = max(error,error1)          # this will be the maximum error in the training set
        

# I get faster convergence if I make the learning rate greater once the error starts to fall
# for the noisy pd data this may be a bad idea
#   if dodecay:
#       if error < errorlast:
#            brain.beta *= 1.0/decayFact
#            brain.alpha *=decayFact
      
                
    errorlast=error
    
    # if it takes ages you should comment out this line because io to terminal is not that fast with idle
      
    print " iteration " ,iter, " max error=",error
    
    if  iter > maxIter:
        print " Reached iteration limit "
        break
    
    if error < tol:
        print " Reached error tolerance "
        break
     
    
#  We can save the state of a brain to a file
#

file=open("greystuff","w")
brain.save(file)
file.close()
