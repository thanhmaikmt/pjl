#
#   Test for BackPropBrain
#
#   I find that sometimes this does not converge (possibly stuck in local a minimum)
#
#   When it does converge it takes about 2000 iterations

from backpropbrain import *

ninputs=2
nhidden=2
nout=2

layerSizes = [ninputs, nhidden, nout]


# These make a lot of difference
# I found these by trail and error.
beta = .001    # learning rate
alpha = 1000.0    # momentum

#Create a brain
brain =BackPropBrain(layerSizes, beta, alpha)

# Training data for an XOR
# 2 inputs and 2 outputs
# the outputs are the XOR and  it's inverse  
TD = [[[0., 0.],[0.,1.0]], \
      [[0.0, 1.0],[1.,0.0]], \
      [[1.0, 0.0],[1.,0.0]], \
      [[1.0, 1.0],[0.,1.0]]]


iter=0
maxIter=200000
tol = 0.000001     # acceptable error in any output ?
errorlast=0.0
dodecay=True
decayFact=.995
while True:   # loop until happiness is found or we exceed maxIter 
    
    iter += 1
    error= 0.0      # 
        
    for td in TD:  # loop on all the training data
        error=brain.bpgt(td[0],td[1])     # train for one data set. 
        out = brain.output()
        
        
        #for i in range(len(td[1])):
        #    error = max(error, abs(td[1][i] - out[i]))
    
    if dodecay:
        if error < errorlast:
            brain.beta *= 1.0/decayFact
            brain.alpha *=decayFact
      
        
            
    errorlast=error
        
    print " iteration " ,iter, " max error=",error
    if  iter > maxIter or error < tol:
       	 break
     
# sanity check !!!

print "--- checking output for training set . . . "

for td in TD:
    o=brain.ffwd(td[0])
    print td[0],td[1],o

# Test save and restore

file=open("greystuff","w")
brain.save(file)
file.close()


file=open("greystuff","r")
clone=loadBrain(file)
file.close()

# sanity check !!!
print "--- checking reloaded brain . . . "
for td in TD:
    o=clone.ffwd(td[0])
    print td[0],td[1],o
