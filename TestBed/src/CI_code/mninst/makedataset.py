import numpy
import cPickle
import gzip
       
# compressed data 
data="mnist.pkl.gz"
f=gzip.open(data)
    
    # load data into the 3 data sets
print " LOADING .....  DATA . . . . . ",
training_set,validation_set,test_set=cPickle.load(f)    
print " DONE"

ntrain1=len(training_set[0])
ntest1=len(test_set[0])

train=[[][]]

test=[[][]]


train_step=50

cnt=0
for i in range(0,ntrain1,train_step):
    train[0].append(training_set[]


