
import pickle

class A:
    def say(self):
        print "I am A"
        
fout=open("XXX",'w')

a=A()

pickle.dump(A,fout)
pickle.dump(a,fout)
fout.close()