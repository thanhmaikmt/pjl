import PIL.Image
import gzip
import cPickle
from numpy import *
print "Hello"

data="mnist.pkl.gz"

f=gzip.open(data)

t,v,test=cPickle.load(f)

x=reshape(t[0][0],(28,28))
x=x*256.0
image=PIL.Image.fromarray(x)
image.show()

