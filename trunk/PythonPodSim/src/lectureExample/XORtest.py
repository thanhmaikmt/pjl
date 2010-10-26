from backpropbrain import *

# 3 layers   2 inputs  1 hidden layer with 2 neurons  1 output
layerSizes = [2, 2, 2]
beta = .001    # learning rate
alpha = 500    # momentum

if alpha*beta > 1.0:
    print " This is probably going to be unstable !!!!! "

#Create a brain
brain =BackPropBrain(layerSizes, beta, alpha)

# Training data for an XOR  
TD = [[[0., 0.],[0.,1.0]], \
      [[0, 1],[1.,0.0]], \
      [[1, 0],[1.,0.0]], \
      [[1, 1],[0.,1.0]]]


iter=0

while True:   # loop until happiness is found 
    
    iter += 1
    error= 0.0
        
    for td in TD:  # loop on all the training data
        brain.bpgt(td[0],td[1])     # 
        out = brain.output()
        #print out
        for i in range(len(td[1])):
            error = max(error, abs(td[1][i] - out[i]))
            
    print " iteration " ,iter, " max error=",error
    if error < .01 :
       	 break
     
# sanity check !!!
for td in TD:
    o=brain.ffwd(td[0])
    print td[0] , td[1] , o
