#
#   Test for BackPropBrain
#
#   I find that sometimes this does not converge (possibly stuck in local a minimum)
#
#   When it does converge it takes about 2000 iterations
#   
#   Each run starts with random weights so just keep trying until it does converge.


from backpropbrain import *

#  Training data a boolean function
#  3 inputs and 2 outputs      8 training examples
TD = [[[0., 0. , 0.],[0.,1.0]],   \
      [[0.0, 0.0 ,1.0],[1.,0.0]], \
      [[0.0 , 1.0, 0.0 ],[1.,0.0]], \
      [[0.0 , 1.0, 1.0],[0.,1.0]],  \
      [[1., 0. , 0.],[1.,0.0]],   \
      [[1.0, 0.0 ,1.0],[0.,1.0]], \
      [[1.0 , 1.0, 0.0 ],[0.,1.0]], \
      [[1.0 , 1.0, 1.0],[1.,.0]]]


ninputs=len(TD[0][0])     #   3
nhidden=4
nout=len(TD[0][1])        #   2

layerSizes = [ninputs, nhidden, nout]


# These make a lot of difference
# I found these by trail and error.
beta = .001    # learning rate
alpha = 1000.0    # momentum

#Create a brain
brain =BackPropBrain(layerSizes, beta, alpha)

iter=0
maxIter=200000
tol = 0.0001     # acceptable error  = 1/2 SUM error_i*error_i
                   # for a real / noisy data set this may be too big.
                     
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
    if dodecay:
        if error < errorlast:
            brain.beta *= 1.0/decayFact
            brain.alpha *=decayFact
      
        
            
    errorlast=error
        
    print " iteration " ,iter, " max error=",error
    
    if  iter > maxIter:
        print " Reached iteration limit "
        break
    
    if error < tol:
        print " Reached error tolerance "
        break
     
    
# sanity check !!!
#
# Note that output values will not be exactly 0 or 1 but if we have converged they should be nearly right

print "--- checking output for training set . . . "

print "    input         target           actual     "
for td in TD:
    o=brain.ffwd(td[0])
    print td[0],td[1],o

#  We can save the state of a brain to a file
#
file=open("greystuff","w")
brain.save(file)
file.close()

# and we can reload it

file=open("greystuff","r")
clone=loadBrain(file)     #   clone should be a copy of the brain we just  
file.close()

# sanity check !!!
print "--- checking reloaded brain . . . "
print "    input         target           actual     "
for td in TD:
    o=clone.ffwd(td[0])
    print td[0],td[1],o
