'''
Created on 18 Dec 2010

@author: pjl
'''

import pickle


class X:
    def hello(self):
        print "hello"
        
        
        
x=X()

file=open("X","w")

pickle.dump(x,file)