from pyo import *
from inspect import *



# Proxy class to provide a view of a Node for the GA
class Proxy:
    
    
    
class Factory:
    
    def __init__(self):
        print "Hello"
        self.tables=[CosTable,SquareTable]
        self.generators = [FM,Sine,SineLoop] 
        self.triggers = [Metro,Beat]
        
        for t in self.generators:
            print t
            print getargspec(t.__init__)
            


factory = Factory()
        