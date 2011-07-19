import gzip
import cPickle
import numpy
import time

def calc_dist(a,b):
    dist=0
    for i in range(len(a)):
        dist+=(a[i]-b[i])**2
    return dist

def calc_dist2(a,b):
    c=a-b
    return (c*c).sum()
    
# compressed data
data="mnist.pkl.gz"

f=gzip.open(data)

# load data into the 3 data sets
print " LOADING .....",
training_set,validation_set,test_set=cPickle.load(f)    
print " DONE"


BIG=1e32


class MinValueKeeper:
    
    
    def __init__(self,k):
        self.table=k*[(BIG,-1)]    # to keep a record of k most minimum vales (fill with something just to get started) 
        self.k=k                   # number of best to keep
        self.minval=1e32           # will store the largest of the k values
        
        
    def add(self,val,key):
        for i in range(k):
            if val< self.table[i]:
                self.table.insert(i,(val,key))
                break
                    
        self.table.pop()         # discard the last entry
        
        
    
    def vote(self):
        for i in range(k):
            
            
        
    
         

nTrain=100
nTest=10

nCorrect=0

training_input=numpy.array(training_set[0])
#training_input=training_set[0]
test_input=numpy.array(test_set[0])
#test_input=test_set[0]


test_output=test_set[1]
training_output=training_set[1] 

start=time.time()

k=4
BIG=1e32

for i in range(nTest):
    jNearest[] = k*[-1]
    mindist [] = k*[BIG]
    
    for j in range(nTrain):
        dist=calc_dist2(training_input[j],test_input[i])
        if dist < mindist:
            mindist=dist
            jNearest=j

        
    print training_output[jNearest],test_output[i]
        
    if  training_output[jNearest] == test_output[i]:
        nCorrect += 1
        
end=time.time()

print nCorrect," out of ",nTest, " In ",end-start," secs"
