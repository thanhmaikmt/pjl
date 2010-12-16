#Partially Dr.Leonards code, but readTraining data was written by me


from backpropbrain import *



def readTrainingData(file):
    TD=[]
    iter=0
    while True:
        
        line=file.readline()
        if len(line) == 0:
            print "Read in lines:" +str(iter)
            return TD
             
        toks=line.split()
    
        input = []
        output = []
        iter+= 1
        
        
                
        if line.isspace() or len(line)==0:
           return points
        toks = line.split(',')
        cont_out=0
        cont_in=0
        for tok in toks:
           #print tok
           if len(tok) != 0 and not tok.isspace() :
                if cont_out == 1:
                   #print "control"+str(tok)
                   output.append(float(tok))
                if tok == "Control":
                   cont_out=1
                   cont_in=0
                   #print "control found" 
                if cont_in == 1:
                   input.append(float(tok))
                   #print "input"+str(tok) 
                if tok == "Input":
                   cont_in=1
        
        
        TD.append([input,output])
        
    
    

#  Use your own numbers here
ninputs=11
nhidden=2
nout=4   


file_in=open("Training.csv","r")

TD = readTrainingData(file_in)
print TD

layerSizes = [ninputs, nhidden, nout]


# These make a lot of difference
# I found these by trail and error.
beta = .00001    # learning rate
alpha =100.0    # momentum

#Create a brain
brain =BackPropBrain(layerSizes, beta, alpha)

iter=0
maxIter=10000

# acceptable error  = 1/2 SUM error_i*error_i
# for a real / noisy data set this may be too big.
# you will need to experiment with this value
tol = 0.232 
                     
# these are used to accelerated search once error starts to fall
dodecay=False                # switch off by setting this to False
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

file=open("greystuff_Car","w")
brain.save(file)
file.close()
