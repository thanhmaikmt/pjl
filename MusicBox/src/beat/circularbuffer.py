import numpy as np


class CircularBuffer():
    def __init__(self , n , dtype = 'f'):
      
        self.array = np.zeros(n*2 , dtype = dtype)
        self.tail=n
        self.N=n
        self.cnt=0
       

    def append(self, a):
        self.cnt+=1
        if self.tail < self.N*2:
            self.array[self.tail] = a
            self.tail += 1
        else:
           
            self.array[:self.N] = self.array[self.N:]
            self.array[self.N] = a
            self.tail = self.N + 1
  
    def replace(self, a):
        self.array[self.tail] = a
            
    def append_array(self,a):
        for x in a:
            self.append(x)
            
    def get_head(self):
        return self.array[self.tail]
        
    def get_window(self):
        return self.array[self.tail-self.N:self.tail]

    def get_count(self):
        return self.cnt 
    
if __name__ == "__main__": 
    n=10          
    
    c  = CircularBuffer( n, dtype = 'f')
    
    for i in range(44):
        c.append(i)
        print c.getWindow()
        
    
    c.append_array([1,2,3,5,6])
    
    print c.getWindow()
