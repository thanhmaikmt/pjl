#
#
#   showing how to save an object

import pickle

class AThing:
    
    def __init__(self,name):
        self.name=name
        
        
a=AThing("Kermit")

fout=open("AThing.dat",'w')

pickle.dump(a,fout)

fout.close()

fin=open("AThing.dat",'r')

b=pickle.load(fin)

fin.close()

print b.name