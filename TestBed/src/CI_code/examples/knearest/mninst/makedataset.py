import numpy
import cPickle as pickle
import gzip
       
# compressed data 
data_orig="mnist.pkl.gz"
f_orig=gzip.open(data_orig)
    
    # load data into the 3 data sets
print " LOADING . . . . . ",
training_set,validation_set,test_set=pickle.load(f_orig)    
print " DONE"

ntrain_orig=len(training_set[0])
ntest_orig=len(test_set[0])

ntrain=1000
ntest=200

train=[[],[]]
test=[[],[]]


train_step=ntrain_orig/ntrain
test_step=ntest_orig/ntest

for i in range(0,ntrain_orig,train_step):
    train[0].append(training_set[0][i])
    train[1].append(training_set[1][i])


for i in range(0,ntest_orig,test_step):
    test[0].append(test_set[0][i])
    test[1].append(test_set[1][i])


data = "mnist_lite.pkl.gz"
f=gzip.open(data,"w")

pickle.dump((train,None,test),f)

f.close()

