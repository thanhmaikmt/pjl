import math
import time
import random

class StressMonitor:

    def __init__(self):
        self.t1c=time.clock()
        self.t1u=time.time()
    
            
    def doit(self):
        t2c=time.clock()
        t2u=time.time()
        stress=(t2c-self.t1c)/(t2u-self.t1u)
        self.t1c=t2c
        self.t1u=t2u
        return stress
    
        

if __name__ == "__main__":   
    stress=StressMonitor()
    
    def work3():
        return random.random()
    
    
    def work2():
        sum=1.0
        for i in range(1000):
            sum*=work3()
        return sum
    
    def work():
        sum1=0.0
        sum2=0.0
        sum3=0.0
        for i in range(1000):
            sum1=work2()
            sum2=work2()
            sum3=sum1*sum2
        
        return sum3
        
        
    for i in range(10000):
        work()
        time.sleep(.1)
        print stress.doit()
    