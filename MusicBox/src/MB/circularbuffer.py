import numpy as np


class CircularBuffer():
    """
    circular buffer.
    Uses an array of twice the maxium history so we always hacve a contiguous array to return.
    """ 
    
    def __init__(self , n , dtype = 'f'):
      
        self.array = np.zeros(n*2 , dtype = dtype)
        self.tail=n
        self.N=n
        self.cnt=0
       

    def append(self, a):
        """
        appends a value to the end of the buffer.
        """
        self.cnt+=1
        if self.tail < self.N*2:   # not at the end just insert a value.
            self.array[self.tail] = a
            self.tail += 1
        else:                      # hist the end. copy second half to the buffer start and set pointer to append from there 
            self.array[:self.N] = self.array[self.N:]
            self.array[self.N] = a
            self.tail = self.N + 1
  
    def replace(self, a):
        """
        Replace the last value.
        """
        self.array[self.tail] = a
            
    def append_array(self,a):
        """
        Append a list to the buffer.
        """
        for x in a:
            self.append(x)
            
    def get_head(self):
        """
        return the last value we appended
        """
        return self.array[self.tail]
        
    def get_window(self):
        """
        Return an array containing the history 
        """
        return self.array[self.tail-self.N:self.tail]

    def get_count(self):
        return self.cnt 
    
if __name__ == "__main__": 
    n=10          
    
    c  = CircularBuffer( n, dtype = 'f')
    
    for i in range(44):
        c.append(i)
        print c.get_window()
        
    
    c.append_array([1,2,3,5,6])
    
    print c.get_window()
